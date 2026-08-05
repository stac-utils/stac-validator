import io
import json
import logging
import os
import sys
import time
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from typing import Any, Dict, List, Optional, Set, Tuple

import click
import fastjsonschema  # type: ignore
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .utilities import validate_with_ref_resolver

# Standard Python logger for FastAPI/Uvicorn integration
logger = logging.getLogger(__name__)

# --- Caches & Config ---
SCHEMA_CACHE: Dict[str, Any] = {}
VALIDATOR_CACHE: Dict[Any, Any] = {}
QUIET_MODE: bool = False
# Store cached schemas inside the repository under local_schemas/.schemas (project-root relative)
LOCAL_SCHEMA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "local_schemas",
    ".schemas",
)

# Shared HTTP session with keep-alive connection pooling and retries for crawler workloads.
HTTP_SESSION = requests.Session()
_http_retries = Retry(
    total=3,
    backoff_factor=0.2,
    status_forcelist=[500, 502, 503, 504],
)
_http_adapter = HTTPAdapter(
    pool_connections=100,
    pool_maxsize=100,
    max_retries=_http_retries,
)
HTTP_SESSION.mount("http://", _http_adapter)
HTTP_SESSION.mount("https://", _http_adapter)
HTTP_SESSION.headers.update({"User-Agent": "stac-fast-cli/5.0"})


def get_local_path_for_uri(uri: str) -> str:
    """Creates a safe local filepath for a cached schema URL."""
    safe_filename = uri.replace("https://", "").replace("http://", "").replace("/", "_")
    return os.path.join(LOCAL_SCHEMA_DIR, safe_filename)


def fetch_schema(uri: str) -> Dict[str, Any]:
    """The Ultimate Handler: RAM -> Disk -> Network -> Disk -> RAM"""

    # 1. RAM Cache
    if uri in SCHEMA_CACHE:
        return SCHEMA_CACHE[uri]

    local_path = get_local_path_for_uri(uri)

    # 2. Disk Cache
    if os.path.exists(local_path):
        try:
            with open(local_path, "r") as f:
                schema_dict = json.load(f)
                SCHEMA_CACHE[uri] = schema_dict
                return schema_dict
        except Exception:
            pass  # If corrupted, fallback to network

    # 3. Network Fetch
    if not QUIET_MODE:
        click.secho(f"    [Network] Fetching: {uri}", fg="yellow", dim=True)
    logger.debug(f"Network cache miss. Fetching schema: {uri}")
    try:
        response = HTTP_SESSION.get(uri, timeout=10)
        response.raise_for_status()
        schema_dict = response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Could not resolve schema: {uri}. Reason: {e}")

    # 4. Save to Disk Cache
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    try:
        with open(local_path, "w") as f:
            json.dump(schema_dict, f)
    except IOError:
        pass  # If we can't write to disk, no big deal, keep going

    # 5. Save to RAM Cache
    SCHEMA_CACHE[uri] = schema_dict
    return schema_dict


def optimize_schema_for_compiler(schema: Any, remove_allof: bool = False) -> Any:
    """
    Recursively patches STAC schemas in-memory to bypass fastjsonschema code generation bugs.
    Strips problematic constructs that cause IndentationError when compiling complex schemas.

    Args:
        schema: The JSON schema dictionary to optimize
        remove_allof: If True, also remove allOf/oneOf/anyOf (used for all schemas)
    """
    if isinstance(schema, list):
        return [optimize_schema_for_compiler(item, remove_allof) for item in schema]

    if isinstance(schema, dict):
        cleaned = {}
        for k, v in schema.items():
            # BUG FIX 1: fastjsonschema crashes on the 'duration' format (fixes product extension)
            if k == "format" and v == "duration":
                continue

            # BUG FIX 2: fastjsonschema writes invalid Python code (empty for/else blocks)
            # when translating complex JSON Schema conditionals (fixes file & storage extensions)
            if k in (
                "if",
                "then",
                "else",
                "dependencies",
                "dependentRequired",
                "dependentSchemas",
            ):
                continue

            # BUG FIX 3: Remove allOf/oneOf/anyOf at top level when requested
            # These cause IndentationError in fastjsonschema's code generator
            if remove_allof and k in ("allOf", "oneOf", "anyOf") and len(schema) > 1:
                # Only skip if there are other validation keywords
                continue

            cleaned[k] = optimize_schema_for_compiler(v, remove_allof)
        return cleaned

    return schema


def get_validator(stac_type: str, stac_version: str, extensions: List[str]):
    """Builds and caches a validator based on Object Type, Version, and Extensions."""
    ext_key = tuple(sorted(extensions))
    cache_key = (stac_type, stac_version, ext_key)

    if cache_key in VALIDATOR_CACHE:
        return VALIDATOR_CACHE[cache_key], True

    # Determine base schema URI
    stac_type_lower = stac_type.lower()
    if stac_type_lower in ["item", "feature"]:
        base_uri = f"https://schemas.stacspec.org/v{stac_version}/item-spec/json-schema/item.json"
    elif stac_type_lower == "collection":
        base_uri = f"https://schemas.stacspec.org/v{stac_version}/collection-spec/json-schema/collection.json"
    elif stac_type_lower == "catalog":
        base_uri = f"https://schemas.stacspec.org/v{stac_version}/catalog-spec/json-schema/catalog.json"
    else:
        raise ValueError(f"Unknown STAC type for validation: {stac_type}")

    # Fetch the raw Base Schema directly
    raw_base_schema = fetch_schema(base_uri)

    try:
        # Tier 1: Try to compile with standard patching first
        optimized_base = optimize_schema_for_compiler(raw_base_schema)
        base_validator = fastjsonschema.compile(
            optimized_base, handlers={"http": fetch_schema, "https": fetch_schema}
        )
        logger.debug(
            f"Base schema {stac_type} {stac_version} compiled with fastjsonschema"
        )
    except Exception:
        try:
            # Tier 2: If it fails, try aggressive patching (stripping allOf/oneOf/anyOf)
            optimized_base = optimize_schema_for_compiler(
                raw_base_schema, remove_allof=True
            )
            base_validator = fastjsonschema.compile(
                optimized_base, handlers={"http": fetch_schema, "https": fetch_schema}
            )
            logger.debug(
                f"Base schema {stac_type} {stac_version} compiled with fastjsonschema (aggressive patching)"
            )
        except Exception:
            # Tier 3: THE ULTIMATE FALLBACK
            # If fastjsonschema completely chokes, instantiate a cached jsonschema validator
            # that is strictly wired to use our high-speed fetch_schema session.
            import jsonschema

            resolver = jsonschema.RefResolver(
                base_uri=base_uri,
                referrer=raw_base_schema,
                handlers={"http": fetch_schema, "https": fetch_schema},
            )
            ValidatorClass = jsonschema.validators.validator_for(raw_base_schema)

            # Pre-compile the jsonschema object ONCE, outside the execution loop
            js_validator = ValidatorClass(raw_base_schema, resolver=resolver)

            def base_validator(data):
                js_validator.validate(data)

            logger.debug(
                f"Base schema {stac_type} {stac_version} compiled with cached jsonschema fallback"
            )

    ext_validators = []
    skipped_extensions = []

    if extensions:
        logger.info(
            f"Warming STAC Validator Cache: Compiling {len(extensions)} extension(s) for {stac_type} {stac_version}..."
        )
        if not QUIET_MODE:
            click.secho(
                f"    [Extensions] Compiling {len(extensions)} extension(s):",
                fg="cyan",
                dim=True,
            )

    for ext in extensions:
        try:
            # 1. Fetch the raw dictionary
            raw_ext_schema = fetch_schema(ext)

            # 2. Try to compile without patching first
            try:
                ext_val = fastjsonschema.compile(
                    raw_ext_schema,
                    handlers={"http": fetch_schema, "https": fetch_schema},
                )
            except Exception:
                # If compilation fails, try with aggressive patching (remove allOf/oneOf/anyOf)
                optimized_schema = optimize_schema_for_compiler(
                    raw_ext_schema, remove_allof=True
                )
                ext_val = fastjsonschema.compile(
                    optimized_schema,
                    handlers={"http": fetch_schema, "https": fetch_schema},
                )

            ext_validators.append(ext_val)
            logger.debug(f"Successfully compiled STAC extension: {ext}")
            if not QUIET_MODE:
                click.secho(f"      ✅ {ext}", fg="green", dim=True)
        except Exception as e:
            # Log to standard Python logging for FastAPI/Uvicorn integration
            logger.warning(
                f"Skipped extension due to compiler incompatibility: {ext} - {type(e).__name__}: {str(e)[:100]}"
            )
            # Safety net for genuinely broken URLs or unfixable schemas
            if not QUIET_MODE:
                click.secho(
                    f"      ❌ {ext}: {type(e).__name__}",
                    fg="red",
                    dim=True,
                )
            skipped_extensions.append(ext)

    if skipped_extensions and not QUIET_MODE:
        click.secho(
            f"    [Warning] Skipped {len(skipped_extensions)} extension(s) due to fastjsonschema incompatibility:",
            fg="yellow",
            dim=True,
        )
        for ext in skipped_extensions:
            click.secho(f"      - {ext}", fg="yellow", dim=True)
        click.secho(
            "    For strict validation of all extensions, use: stac-valid validate <file>",
            fg="yellow",
            dim=True,
        )

    def validator(data: Dict[str, Any]) -> None:
        old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        try:
            # Execute the pre-compiled native Python functions
            base_validator(data)
            for ext_val in ext_validators:
                ext_val(data)
        finally:
            sys.setrecursionlimit(old_limit)

    # Cache the resulting validator so future items use it instantly
    VALIDATOR_CACHE[cache_key] = validator
    return validator, False


class FastValidator:
    def __init__(
        self,
        stac_file: str,
        quiet: bool = False,
        verbose: bool = False,
        limit: Optional[int] = None,
        validate_geometry: bool = False,
    ):
        global QUIET_MODE
        self.stac_file = stac_file
        self.quiet = quiet
        self.valid = True
        self.verbose = verbose
        self.limit = limit
        self.validate_geometry = validate_geometry
        self.message: List[Dict[str, Any]] = []
        QUIET_MODE = quiet

    def _validate_datetime_range(self, data: Dict[str, Any]) -> None:
        """Ensures start_datetime is not strictly after end_datetime per STAC Spec.

        Uses lexicographical string comparison since RFC 3339 timestamps sort
        chronologically when compared as strings. This avoids datetime parsing
        issues in Python 3.8/3.9 with non-standard ISO 8601 formats.
        """
        if data.get("type") != "Feature":
            return

        properties = data.get("properties", {})
        start_str = properties.get("start_datetime")
        end_str = properties.get("end_datetime")

        if start_str and end_str:
            # RFC 3339 timestamps sort lexicographically, so we can compare as strings
            # This avoids datetime.fromisoformat() parsing issues in Python 3.8/3.9
            if start_str > end_str:
                raise ValueError(
                    f"Logical Error: start_datetime ({start_str}) cannot be strictly after end_datetime ({end_str})"
                )

    def _validate_geometry(self, data: Dict[str, Any]) -> None:
        """Lightweight topology check for global bounds and antimeridian crossings."""
        if data.get("type") != "Feature":
            return

        geometry = data.get("geometry")
        if not geometry:
            return

        geom_type = geometry.get("type")
        coords = geometry.get("coordinates")
        if not coords or geom_type not in ("Polygon", "MultiPolygon"):
            return

        def check_bounds(c: list):
            if not c:
                return
            if isinstance(c[0], (int, float)):
                if not (-180 <= c[0] <= 180) or not (-90 <= c[1] <= 90):
                    raise ValueError(f"Geometry out of global WGS84 bounds: {c}")
            else:
                for sub in c:
                    check_bounds(sub)

        check_bounds(coords)

        def check_rings(rings: list):
            max_vertices = int(os.environ.get("MAX_TOPOLOGY_VERTICES", 5000))
            for ring in rings:
                if len(ring) < 4:
                    raise ValueError("Polygon ring must have at least 4 coordinates.")
                if len(ring) > max_vertices:
                    raise ValueError(
                        f"Geometry exceeds maximum allowed vertices ({max_vertices}). Found {len(ring)}."
                    )
                for i in range(len(ring) - 1):
                    if abs(ring[i][0] - ring[i + 1][0]) > 180:
                        raise ValueError(
                            f"Improper antimeridian crossing between {ring[i][0]} and {ring[i + 1][0]}"
                        )

        if geom_type == "Polygon":
            check_rings(coords)
        elif geom_type == "MultiPolygon":
            for poly in coords:
                check_rings(poly)

    def _limit_reached(self, results: List[Dict]) -> bool:
        return self.limit is not None and len(results) >= self.limit

    def _get_base_schema_uri(self, stac_type: str, stac_version: str) -> str:
        stac_type_lower = stac_type.lower()
        if stac_type_lower in ["item", "feature"]:
            return f"https://schemas.stacspec.org/v{stac_version}/item-spec/json-schema/item.json"
        if stac_type_lower == "collection":
            return f"https://schemas.stacspec.org/v{stac_version}/collection-spec/json-schema/collection.json"
        if stac_type_lower == "catalog":
            return f"https://schemas.stacspec.org/v{stac_version}/catalog-spec/json-schema/catalog.json"
        raise ValueError(f"Unknown STAC type for validation: {stac_type}")

    def _is_ref_resolution_error(self, err: Exception) -> bool:
        err_text = str(err)
        err_type = err.__class__.__name__
        return (
            "Unresolvable JSON pointer" in err_text
            or "RefResolutionError" in err_type
            or "Unresolvable" in err_type
        )

    def _validate_with_jsonschema_fallback(
        self,
        item: Dict[str, Any],
        stac_type: str,
        stac_version: str,
        extensions: List[str],
    ) -> None:
        """Fallback validation path using the main jsonschema resolver utility."""
        base_schema = self._get_base_schema_uri(stac_type, stac_version)
        validate_with_ref_resolver(base_schema, item)
        for ext_schema in extensions:
            validate_with_ref_resolver(ext_schema, item)

    def _load_json_resource(self, resource_path: str) -> Dict[str, Any]:
        if resource_path.startswith("http"):
            response = HTTP_SESSION.get(resource_path, timeout=15)
            response.raise_for_status()
            return response.json()

        with open(resource_path, "r") as f:
            return json.load(f)

    def _get_parallel_fetch_workers(self, item_count: int) -> int:
        return max(1, min(8, item_count))

    def _load_collection_documents(
        self, collection_urls: List[str]
    ) -> List[Tuple[str, Optional[Dict[str, Any]], Optional[Exception]]]:
        if len(collection_urls) <= 1:
            results_single: List[
                Tuple[str, Optional[Dict[str, Any]], Optional[Exception]]
            ] = []
            for collection_url in collection_urls:
                try:
                    results_single.append(
                        (collection_url, self._load_json_resource(collection_url), None)
                    )
                except Exception as exc:
                    results_single.append((collection_url, None, exc))
            return results_single

        with ThreadPoolExecutor(
            max_workers=self._get_parallel_fetch_workers(len(collection_urls))
        ) as executor:
            futures: List[Future[Dict[str, Any]]] = [
                executor.submit(self._load_json_resource, collection_url)
                for collection_url in collection_urls
            ]

            results_parallel: List[
                Tuple[str, Optional[Dict[str, Any]], Optional[Exception]]
            ] = []
            for collection_url, future in zip(collection_urls, futures):
                try:
                    results_parallel.append((collection_url, future.result(), None))
                except Exception as exc:
                    results_parallel.append((collection_url, None, exc))

        return results_parallel

    def _prefetch_api_collection_resources(
        self, collection_url: str
    ) -> Tuple[str, Optional[Dict[str, Dict[str, Any]]], Optional[Exception]]:
        try:
            collection_data = self._load_json_resource(collection_url)
        except Exception as exc:
            return collection_url, None, exc

        resources = {collection_url: collection_data}
        base_dir = collection_url.rsplit("/", 1)[0]

        for link in collection_data.get("links", []):
            if link.get("rel") != "items":
                continue

            href = link.get("href", "")
            if not href:
                continue

            if href.startswith("http"):
                items_path = href
            else:
                items_path = os.path.normpath(os.path.join(base_dir, href))

            try:
                resources[items_path] = self._load_json_resource(items_path)
            except Exception:
                pass

        return collection_url, resources, None

    def _prefetch_api_collection_resources_batch(
        self, collection_urls: List[str]
    ) -> List[Tuple[str, Optional[Dict[str, Dict[str, Any]]], Optional[Exception]]]:
        if len(collection_urls) <= 1:
            return [
                self._prefetch_api_collection_resources(collection_url)
                for collection_url in collection_urls
            ]

        with ThreadPoolExecutor(
            max_workers=self._get_parallel_fetch_workers(len(collection_urls))
        ) as executor:
            futures: List[
                Future[
                    Tuple[str, Optional[Dict[str, Dict[str, Any]]], Optional[Exception]]
                ]
            ] = [
                executor.submit(self._prefetch_api_collection_resources, collection_url)
                for collection_url in collection_urls
            ]
            return [future.result() for future in futures]

    def run(self):
        """Universal high-speed STAC Validator (Items, Collections, Catalogs, FeatureCollections)"""
        if not self.quiet:
            click.secho(f"\n📂 Loading: {self.stac_file}", fg="blue", bold=True)

        try:
            data = self._load_json_resource(self.stac_file)
        except Exception as e:
            click.secho(f"❌ Error reading {self.stac_file}: {e}", fg="red", bold=True)
            self.valid = False
            return

        # Detect payload structure
        obj_type = data.get("type", "")
        items_to_validate = []

        if obj_type == "FeatureCollection":
            items_to_validate = data.get("features", [])
            if not self.quiet:
                click.secho(
                    f"📦 Detected FeatureCollection ({len(items_to_validate)} Items)\n",
                    fg="cyan",
                )
        elif obj_type == "Feature":
            items_to_validate = [data]
            if not self.quiet:
                click.secho("📄 Detected: STAC Item\n", fg="cyan")
        elif obj_type == "Collection":
            items_to_validate = [data]
            if not self.quiet:
                click.secho("📚 Detected: STAC Collection\n", fg="cyan")
        elif obj_type == "Catalog" or ("id" in data and "description" in data):
            # Fallback for old catalogs missing the 'type' field
            data["type"] = "Catalog"
            items_to_validate = [data]
            if not self.quiet:
                click.secho("🗂️  Detected: STAC Catalog\n", fg="cyan")
        else:
            if "type" in data:
                click.secho(
                    f"❌ Unknown JSON type. Unsupported 'type' value: {obj_type!r}.",
                    fg="red",
                    bold=True,
                )
            else:
                click.secho(
                    "❌ Unknown JSON type. Missing 'type' field.", fg="red", bold=True
                )
            self.valid = False
            return

        # --- Metrics ---
        available_objects = len(items_to_validate)
        if self.limit is not None:
            items_to_validate = items_to_validate[: self.limit]
            if not self.quiet and available_objects > self.limit:
                click.secho(
                    f"🔢 Limiting validation to first {self.limit} objects (out of {available_objects}).",
                    fg="yellow",
                )

        total_setup_ms = 0.0
        total_exec_ms = 0.0
        valid_count = 0
        invalid_count = 0
        error_registry: Dict[str, List[str]] = {}
        stac_versions_found: Set[str] = set()
        schemas_checked: Set[str] = set()

        for index, item in enumerate(items_to_validate):
            # Determine specific STAC attributes for this object
            item_id = item.get("id", f"unknown-{index}")
            stac_version = item.get("stac_version", "1.0.0")
            extensions = item.get("stac_extensions", [])

            # Track versions and schemas
            stac_versions_found.add(stac_version)

            # Map Feature->Item, others keep their type
            actual_type = (
                "Item" if item.get("type") == "Feature" else item.get("type", "Catalog")
            )

            # Build schema URI for this object type
            try:
                base_schema = self._get_base_schema_uri(actual_type, stac_version)
            except ValueError:
                base_schema = ""

            if base_schema:
                schemas_checked.add(base_schema)

            # Track extensions
            for ext in extensions:
                schemas_checked.add(ext)

            # --- Setup Timer ---
            t0 = time.perf_counter()
            try:
                validator, is_cached = get_validator(
                    actual_type, stac_version, extensions
                )
            except Exception as e:
                if not self.quiet:
                    click.secho(f"❌ Setup failed for {item_id}: {e}", fg="red")
                invalid_count += 1
                self.valid = False
                error_msg = f"Setup failed: {str(e)}"
                if error_msg not in error_registry:
                    error_registry[error_msg] = []
                error_registry[error_msg].append(item_id)
                continue
            t1 = time.perf_counter()
            setup_time = (t1 - t0) * 1000
            total_setup_ms += setup_time

            # --- Execution Timer ---
            t2 = time.perf_counter()
            try:
                validator(item)
                # Run logical firewalls
                self._validate_datetime_range(item)
                if self.validate_geometry:
                    self._validate_geometry(item)
                t3 = time.perf_counter()
                exec_time = (t3 - t2) * 1000
                total_exec_ms += exec_time
                valid_count += 1
                status_text = click.style("✅ VALID", fg="green")

            except fastjsonschema.JsonSchemaValueException as e:
                t3 = time.perf_counter()
                exec_time = (t3 - t2) * 1000
                total_exec_ms += exec_time
                invalid_count += 1
                self.valid = False

                # --- The STAC Error Translator ---
                error_msg = f"{e.name} {e.message.replace(e.name, '').strip()}"
                if "disallowed definition" in error_msg:
                    if "collection" in error_msg:
                        error_msg = "STAC Spec Violation: Missing {'rel': 'collection'} in links array."
                    else:
                        error_msg = (
                            f"{e.name} violated a 'not' rule. Value: {repr(e.value)}"
                        )

                # Group errors
                if error_msg not in error_registry:
                    error_registry[error_msg] = []
                error_registry[error_msg].append(item_id)
                status_text = click.style("❌ INVALID", fg="red")

            except ValueError as e:
                t3 = time.perf_counter()
                exec_time = (t3 - t2) * 1000
                total_exec_ms += exec_time
                invalid_count += 1
                self.valid = False

                # Logical validation errors (datetime range, geometry)
                error_msg = str(e)
                if error_msg not in error_registry:
                    error_registry[error_msg] = []
                error_registry[error_msg].append(item_id)
                status_text = click.style("❌ INVALID", fg="red")

            except Exception as e:
                t3 = time.perf_counter()
                exec_time = (t3 - t2) * 1000
                total_exec_ms += exec_time

                if self._is_ref_resolution_error(e):
                    try:
                        self._validate_with_jsonschema_fallback(
                            item,
                            actual_type,
                            stac_version,
                            extensions,
                        )
                        valid_count += 1
                        status_text = click.style("✅ VALID", fg="green")
                    except Exception as fallback_err:
                        invalid_count += 1
                        self.valid = False
                        error_msg = str(fallback_err)
                        if error_msg not in error_registry:
                            error_registry[error_msg] = []
                        error_registry[error_msg].append(item_id)
                        status_text = click.style("❌ INVALID", fg="red")
                else:
                    invalid_count += 1
                    self.valid = False
                    error_msg = str(e)
                    if error_msg not in error_registry:
                        error_registry[error_msg] = []
                    error_registry[error_msg].append(item_id)
                    status_text = click.style("❌ INVALID", fg="red")

            if not self.quiet:
                if self.verbose or index < 5 or (len(items_to_validate) < 20):
                    cache_icon = "⚡" if is_cached else "🐌"
                    click.echo(
                        f"[{index + 1}] ID: {item_id} | Type: {actual_type} | Cache {cache_icon} | Setup: {setup_time:>6.2f}ms | Exec: {exec_time:>5.2f}ms | {status_text}"
                    )
                elif index == 5:
                    click.secho(
                        "... silencing output for remaining items (validating at maximum speed) ...",
                        dim=True,
                    )

        # --- Summary Report ---
        click.echo("\n" + "=" * 55)
        click.secho("📊 VALIDATION SUMMARY", bold=True)
        click.echo("=" * 55)
        click.echo(f"Total Objects Processed : {len(items_to_validate)}")
        click.echo(
            f"Valid Objects           : {click.style(str(valid_count), fg='green')}"
        )

        invalid_color = "red" if invalid_count > 0 else "green"
        click.echo(
            f"Invalid Objects         : {click.style(str(invalid_count), fg=invalid_color)}"
        )

        click.echo("-" * 55)
        click.echo(f"Total Setup Time        : {total_setup_ms:.2f} ms")
        click.echo(f"Total Execution Time    : {total_exec_ms:.2f} ms")
        if len(items_to_validate) > 0:
            click.echo(
                f"Average Exec per Object : {(total_exec_ms / len(items_to_validate)):.3f} ms"
            )

        if invalid_count > 0:
            click.echo("=" * 55)
            click.secho("🚨 ERROR BREAKDOWN", bold=True, fg="red")
            click.echo("=" * 55)
            for err_msg, affected_ids in error_registry.items():
                count = len(affected_ids)
                click.echo(f"\n❌ {click.style(err_msg, fg='yellow', bold=True)}")
                click.echo(
                    f"   Affected Items: {click.style(str(count), fg='red', bold=True)}"
                )
                sample_ids = ", ".join(affected_ids[:3])
                if count > 3:
                    sample_ids += f" ... (and {count - 3} more)"
                click.echo(f"   Examples:       {sample_ids}")

        # Populate the message attribute for API usage (similar to StacValidate)
        self.message = [
            {
                "path": self.stac_file,
                "valid_stac": self.valid,
                "stac_versions": sorted(list(stac_versions_found)),
                "schemas_checked": sorted(list(schemas_checked)),
                "total_objects": len(items_to_validate),
                "valid_objects": valid_count,
                "invalid_objects": invalid_count,
                "setup_time_ms": total_setup_ms,
                "execution_time_ms": total_exec_ms,
                "errors": [
                    {
                        "error_message": err_msg,
                        "affected_items": affected_ids,
                        "count": len(affected_ids),
                    }
                    for err_msg, affected_ids in error_registry.items()
                ],
            }
        ]

        click.echo("\n")

    def run_dict(self, stac_dict: Dict[str, Any], source_name: str = "in-memory"):
        """Validate a native Python dictionary directly without file/network loading."""
        if not isinstance(stac_dict, dict):
            self.valid = False
            self.message = [
                {
                    "path": source_name,
                    "valid_stac": False,
                    "error_message": "Input to run_dict must be a dictionary.",
                }
            ]
            return

        self.stac_file = source_name

        data = dict(stac_dict)
        obj_type = data.get("type", "")
        items_to_validate: List[Dict[str, Any]] = []

        if obj_type == "FeatureCollection":
            features = data.get("features", [])
            items_to_validate = features if isinstance(features, list) else []
        elif obj_type in ["Feature", "Collection"]:
            items_to_validate = [data]
        elif obj_type == "Catalog" or ("id" in data and "description" in data):
            data["type"] = "Catalog"
            items_to_validate = [data]
        else:
            self.valid = False
            if "type" in data:
                error_msg = (
                    f"Unknown JSON type. Unsupported 'type' value: {obj_type!r}."
                )
            else:
                error_msg = "Unknown JSON type. Missing 'type' field."

            self.message = [
                {
                    "path": source_name,
                    "valid_stac": False,
                    "error_message": error_msg,
                }
            ]
            return

        available_objects = len(items_to_validate)
        if self.limit is not None:
            items_to_validate = items_to_validate[: self.limit]

        total_setup_ms = 0.0
        total_exec_ms = 0.0
        valid_count = 0
        invalid_count = 0
        error_registry: Dict[str, List[str]] = {}
        stac_versions_found: Set[str] = set()
        schemas_checked: Set[str] = set()

        self.valid = True

        for index, item in enumerate(items_to_validate):
            item_id = item.get("id", f"unknown-{index}")
            stac_version = item.get("stac_version", "1.0.0")
            extensions = item.get("stac_extensions", [])

            stac_versions_found.add(stac_version)

            actual_type = (
                "Item" if item.get("type") == "Feature" else item.get("type", "Catalog")
            )

            try:
                base_schema = self._get_base_schema_uri(actual_type, stac_version)
            except ValueError:
                base_schema = ""

            if base_schema:
                schemas_checked.add(base_schema)

            for ext in extensions:
                schemas_checked.add(ext)

            t0 = time.perf_counter()
            try:
                validator, _ = get_validator(actual_type, stac_version, extensions)
            except Exception as e:
                invalid_count += 1
                self.valid = False
                error_msg = str(e)
                logger.error(f"Schema setup failed for item {item_id}: {error_msg}")
                if error_msg not in error_registry:
                    error_registry[error_msg] = []
                error_registry[error_msg].append(item_id)
                continue
            t1 = time.perf_counter()
            total_setup_ms += (t1 - t0) * 1000

            t2 = time.perf_counter()
            try:
                validator(item)
                # Run logical firewalls
                self._validate_datetime_range(item)
                if self.validate_geometry:
                    self._validate_geometry(item)
                t3 = time.perf_counter()
                total_exec_ms += (t3 - t2) * 1000
                valid_count += 1
            except fastjsonschema.JsonSchemaValueException as e:
                t3 = time.perf_counter()
                total_exec_ms += (t3 - t2) * 1000
                invalid_count += 1
                self.valid = False
                error_msg = f"{e.name} {e.message.replace(e.name, '').strip()}"
                if "disallowed definition" in error_msg and "collection" in error_msg:
                    error_msg = "STAC Spec Violation: Missing {'rel': 'collection'} in links array."
                if error_msg not in error_registry:
                    error_registry[error_msg] = []
                error_registry[error_msg].append(item_id)
            except ValueError as e:
                t3 = time.perf_counter()
                total_exec_ms += (t3 - t2) * 1000
                invalid_count += 1
                self.valid = False
                error_msg = str(e)
                if error_msg not in error_registry:
                    error_registry[error_msg] = []
                error_registry[error_msg].append(item_id)
            except Exception as e:
                t3 = time.perf_counter()
                total_exec_ms += (t3 - t2) * 1000
                if self._is_ref_resolution_error(e):
                    try:
                        self._validate_with_jsonschema_fallback(
                            item,
                            actual_type,
                            stac_version,
                            extensions,
                        )
                        valid_count += 1
                    except Exception as fallback_err:
                        invalid_count += 1
                        self.valid = False
                        error_msg = str(fallback_err)
                        if error_msg not in error_registry:
                            error_registry[error_msg] = []
                        error_registry[error_msg].append(item_id)
                else:
                    invalid_count += 1
                    self.valid = False
                    error_msg = str(e)
                    if error_msg not in error_registry:
                        error_registry[error_msg] = []
                    error_registry[error_msg].append(item_id)

        self.message = [
            {
                "path": source_name,
                "valid_stac": self.valid,
                "stac_versions": sorted(list(stac_versions_found)),
                "schemas_checked": sorted(list(schemas_checked)),
                "total_objects": len(items_to_validate),
                "valid_objects": valid_count,
                "invalid_objects": invalid_count,
                "setup_time_ms": total_setup_ms,
                "execution_time_ms": total_exec_ms,
                "input_objects": available_objects,
                "errors": [
                    {
                        "error_message": err_msg,
                        "affected_items": affected_ids,
                        "count": len(affected_ids),
                    }
                    for err_msg, affected_ids in error_registry.items()
                ],
            }
        ]

    def run_recursive(self):
        """Recursively validate a local STAC catalog/collection and all its children."""
        sys.setrecursionlimit(10000)
        start_time = time.perf_counter()

        # Load the root STAC object
        try:
            root_data = self._load_json_resource(self.stac_file)
            root_path = (
                self.stac_file
                if self.stac_file.startswith("http")
                else os.path.abspath(self.stac_file)
            )
        except Exception as e:
            click.secho(f"❌ Error reading {self.stac_file}: {e}", fg="red", bold=True)
            self.valid = False
            return

        # Recursively validate the root and all children
        results = []
        visited = set()
        visited.add(root_path)
        self._validate_recursive(root_data, root_path, results, visited, is_api=False)

        if self.limit is not None and not self.quiet and len(results) >= self.limit:
            click.secho(
                f"🔢 Validation limit reached ({self.limit} objects).",
                fg="yellow",
            )

        # Display results
        click.echo("\n" + "=" * 55)
        click.secho("📊 RECURSIVE VALIDATION SUMMARY", bold=True, fg="blue")
        click.echo("=" * 55)

        valid_count = sum(1 for r in results if r["valid_stac"])
        invalid_count = len(results) - valid_count
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        click.echo(f"Total Objects Validated: {len(results)}")
        click.echo(f"Valid Objects:           {valid_count}")
        click.echo(f"Invalid Objects:         {invalid_count}")
        click.echo(f"Execution Time:          {elapsed_ms:.2f} ms")

        if invalid_count > 0:
            click.echo("\n" + "=" * 55)
            click.secho("🚨 INVALID OBJECTS", bold=True, fg="red")
            click.echo("=" * 55)

            # Group errors by message
            error_groups = {}
            for result in results:
                if not result["valid_stac"]:
                    error_msg = result.get("error_message", "Unknown error")
                    if error_msg not in error_groups:
                        error_groups[error_msg] = []
                    # Store both path and ID for better identification
                    object_id = result.get("id", "unknown")
                    error_groups[error_msg].append(
                        {"path": result["path"], "id": object_id}
                    )

            # Display grouped errors
            for error_msg, items in error_groups.items():
                click.echo(f"\n❌ {error_msg}")
                click.echo(f"   Affected Objects: {len(items)}")
                # Show first 5 examples
                for item in items[:5]:
                    item_id = item["id"] if item["id"] != "unknown" else ""
                    if item_id:
                        click.echo(f"   - {item['path']} (ID: {item_id})")
                    else:
                        click.echo(f"   - {item['path']}")
                if len(items) > 5:
                    click.echo(f"   ... and {len(items) - 5} more")

        # Set overall validity
        self.valid = all(r.get("valid_stac", False) for r in results)
        self.message = results

    def run_api(self):
        """Recursively validate a STAC API catalog and all its collections/items."""
        sys.setrecursionlimit(10000)
        start_time = time.perf_counter()

        if not self.quiet:
            click.secho("🚀 Starting STAC API validation...", fg="blue", bold=True)
            click.secho(
                "⏳ Fetching API root and discovery links...", fg="cyan", dim=True
            )

        # Load the root STAC API object
        try:
            root_data = self._load_json_resource(self.stac_file)
            root_path = (
                self.stac_file
                if self.stac_file.startswith("http")
                else os.path.abspath(self.stac_file)
            )
        except Exception as e:
            click.secho(f"❌ Error reading {self.stac_file}: {e}", fg="red", bold=True)
            self.valid = False
            return

        # Recursively validate the root and all children (API mode)
        results = []
        visited = set()
        visited.add(root_path)
        self._progress_count = 0

        if not self.quiet:
            click.secho(
                "🧠 Compiling/warming schemas (first objects may be slower)...",
                fg="cyan",
                dim=True,
            )

        self._validate_recursive(root_data, root_path, results, visited, is_api=True)

        if self.limit is not None and not self.quiet and len(results) >= self.limit:
            click.secho(
                f"🔢 Validation limit reached ({self.limit} objects).",
                fg="yellow",
            )

        # Display results
        click.echo("\n" + "=" * 55)
        click.secho("📊 STAC API VALIDATION SUMMARY", bold=True, fg="blue")
        click.echo("=" * 55)

        valid_count = sum(1 for r in results if r["valid_stac"])
        invalid_count = len(results) - valid_count
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        click.echo(f"Total Objects Validated: {len(results)}")
        click.echo(f"Valid Objects:           {valid_count}")
        click.echo(f"Invalid Objects:         {invalid_count}")
        click.echo(f"Execution Time:          {elapsed_ms:.2f} ms")

        if invalid_count > 0:
            click.echo("\n" + "=" * 55)
            click.secho("🚨 INVALID OBJECTS", bold=True, fg="red")
            click.echo("=" * 55)

            # Group errors by message
            error_groups = {}
            for result in results:
                if not result["valid_stac"]:
                    error_msg = result.get("error_message", "Unknown error")
                    if error_msg not in error_groups:
                        error_groups[error_msg] = []
                    # Store both path and ID for better identification
                    object_id = result.get("id", "unknown")
                    error_groups[error_msg].append(
                        {"path": result["path"], "id": object_id}
                    )

            # Display grouped errors
            for error_msg, items in error_groups.items():
                click.echo(f"\n❌ {error_msg}")
                click.echo(f"   Affected Objects: {len(items)}")
                # Show first 5 examples
                for item in items[:5]:
                    item_id = item["id"] if item["id"] != "unknown" else ""
                    if item_id:
                        click.echo(f"   - {item['path']} (ID: {item_id})")
                    else:
                        click.echo(f"   - {item['path']}")
                if len(items) > 5:
                    click.echo(f"   ... and {len(items) - 5} more")

        # Set overall validity
        self.valid = all(r.get("valid_stac", False) for r in results)
        self.message = results

    def _validate_recursive(
        self,
        data: Dict[str, Any],
        file_path: str,
        results: List[Dict],
        visited: Set[str],
        is_api: bool = False,
        collection_id: Optional[str] = None,
        prefetched_resources: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        """Recursively validate a STAC object and its children.

        Args:
            data: The STAC object to validate
            file_path: Path or URL to the object
            results: List to accumulate validation results
            visited: Set of already-visited paths to prevent circular references
            is_api: If True, follow API-specific links (data, items, next); if False, follow catalog links (child, item)
            collection_id: Optional collection ID for items from FeatureCollections
        """
        if self._limit_reached(results):
            return

        # Log progress in API mode
        if is_api and not self.quiet:
            self._progress_count += 1
            object_id = data.get("id", "unknown")
            object_type = data.get("type", "unknown")
            if collection_id and object_type == "Feature":
                click.secho(
                    f"  [{self._progress_count}] Validating {object_type}: {object_id} (Collection: {collection_id})",
                    fg="cyan",
                    dim=True,
                )
            else:
                click.secho(
                    f"  [{self._progress_count}] Validating {object_type}: {object_id}",
                    fg="cyan",
                    dim=True,
                )

        # Determine STAC type - could be "Catalog", "Collection", or "Feature" (Item)
        raw_type = data.get("type", "unknown")
        if raw_type == "Feature":
            stac_type = "item"
        elif raw_type == "Collection":
            stac_type = "collection"
        elif raw_type == "Catalog":
            stac_type = "catalog"
        else:
            stac_type = raw_type.lower() if raw_type else "unknown"

        stac_version = data.get("stac_version", "unknown")

        # Validate current object using get_validator (same as run() does)
        # Skip validation for STAC API responses (they have conformsTo instead of stac_extensions)
        is_stac_api = "conformsTo" in data

        if is_stac_api:
            # STAC API catalogs don't validate against STAC schemas, just mark as valid
            is_valid = True
            error_msg = None
        else:
            try:
                extensions = data.get("stac_extensions", [])

                # Mute noisy "[Fallback]" and "[Network]" prints from validation execution path
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    validator, _ = get_validator(stac_type, stac_version, extensions)
                    validator(data)

                is_valid = True
                error_msg = None
            except fastjsonschema.JsonSchemaValueException as e:
                is_valid = False
                error_msg = f"{e.name} {e.message.replace(e.name, '').strip()}"
            except Exception as e:
                if self._is_ref_resolution_error(e):
                    try:
                        self._validate_with_jsonschema_fallback(
                            data,
                            stac_type,
                            stac_version,
                            extensions,
                        )
                        is_valid = True
                        error_msg = None
                    except Exception as fallback_err:
                        is_valid = False
                        error_msg = str(fallback_err)
                else:
                    is_valid = False
                    error_msg = str(e)

        # Create result for this object
        # Extract ID if available
        object_id = data.get("id", "unknown")

        result = {
            "path": file_path,
            "id": object_id,
            "valid_stac": is_valid,
            "stac_type": stac_type,
            "stac_version": stac_version,
        }
        if error_msg:
            result["error_message"] = error_msg

        results.append(result)

        if self._limit_reached(results):
            return

        # Process child links
        base_dir = (
            os.path.dirname(file_path)
            if not file_path.startswith("http")
            else file_path.rsplit("/", 1)[0]
        )
        links = data.get("links", [])

        for link in links:
            if self._limit_reached(results):
                break

            rel = link.get("rel", "")
            href = link.get("href", "")

            # Determine if we should follow this link based on mode
            should_follow = False
            if is_api:
                # API mode: follow "data" (collections), "child", "item", and "items" links
                if rel in ["data", "child", "item", "items"] and href:
                    should_follow = True
            else:
                # Local mode: follow "child" and "item" links only
                if rel in ["child", "item"] and href:
                    should_follow = True

            if should_follow:
                # Resolve relative path
                if href.startswith("http"):
                    child_path = href
                else:
                    child_path = os.path.normpath(os.path.join(base_dir, href))

                if child_path in visited:
                    continue
                visited.add(child_path)

                # Load and validate child
                try:
                    if prefetched_resources and child_path in prefetched_resources:
                        child_data = prefetched_resources[child_path]
                    else:
                        if is_api and not self.quiet and rel in ["data", "items"]:
                            label = "collections" if rel == "data" else "items"
                            click.secho(
                                f"  Discovering {label}: {child_path}",
                                fg="cyan",
                                dim=True,
                            )
                        child_data = self._load_json_resource(child_path)

                    # If this is a collections list endpoint, extract individual collections
                    if rel == "data" and is_api and isinstance(child_data, dict):
                        collections = child_data.get("collections", [])
                        if collections:
                            # This is a collections list - process each collection
                            collection_urls = []
                            for collection in collections:
                                collection_id = collection.get("id")
                                if collection_id:
                                    collection_urls.append(
                                        f"{child_path.rstrip('/')}/{collection_id}"
                                    )

                            # Avoid prefetching beyond remaining validation capacity.
                            if self.limit is not None:
                                remaining = max(1, self.limit - len(results))
                                collection_urls = collection_urls[:remaining]

                            for (
                                collection_url,
                                prefetched_collection_resources,
                                load_error,
                            ) in self._prefetch_api_collection_resources_batch(
                                collection_urls
                            ):
                                if self._limit_reached(results):
                                    break

                                if load_error is not None:
                                    results.append(
                                        {
                                            "path": collection_url,
                                            "valid_stac": False,
                                            "error_message": f"Failed to load: {str(load_error)}",
                                        }
                                    )
                                    continue

                                visited.add(collection_url)
                                if prefetched_collection_resources is None:
                                    continue
                                collection_data = prefetched_collection_resources[
                                    collection_url
                                ]

                                self._validate_recursive(
                                    collection_data,
                                    collection_url,
                                    results,
                                    visited,
                                    is_api,
                                    prefetched_resources=prefetched_collection_resources,
                                )
                        else:
                            # Not a collections list, validate as normal
                            self._validate_recursive(
                                child_data, child_path, results, visited, is_api
                            )
                    # If this is an items endpoint (GeoJSON FeatureCollection), validate only Features
                    elif rel == "items" and is_api and isinstance(child_data, dict):
                        features = child_data.get("features")

                        # Extract collection ID from URL (e.g., /collections/{id}/items)
                        collection_id_from_items: Optional[str] = None
                        if "/collections/" in child_path:
                            parts = child_path.split("/collections/")
                            if len(parts) > 1:
                                collection_parts = parts[1].split("/items")
                                collection_id_from_items = (
                                    collection_parts[0] if collection_parts else None
                                )

                        # Validate each feature item from the items page, not the FeatureCollection container.
                        if isinstance(features, list):
                            for feature in features:
                                if self._limit_reached(results):
                                    break

                                item_id = feature.get("id", "unknown")
                                item_path = f"{child_path}#{item_id}"
                                self._validate_recursive(
                                    feature,
                                    item_path,
                                    results,
                                    visited,
                                    is_api,
                                    collection_id_from_items,
                                )
                    else:
                        # Recursively validate child
                        self._validate_recursive(
                            child_data, child_path, results, visited, is_api
                        )
                except Exception as e:
                    if self._limit_reached(results):
                        break

                    results.append(
                        {
                            "path": child_path,
                            "valid_stac": False,
                            "error_message": f"Failed to load: {str(e)}",
                        }
                    )
