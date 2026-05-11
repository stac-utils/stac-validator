import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from typing import Any, Dict, List, Set

import click
import fastjsonschema  # type: ignore

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
    req = urllib.request.Request(uri, headers={"User-Agent": "stac-fast-cli/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            schema_dict = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
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

    schema_fragments: List[Dict[str, str]] = [{"$ref": base_uri}]
    for ext in extensions:
        schema_fragments.append({"$ref": ext})
    dynamic_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "allOf": schema_fragments,
    }

    try:
        validator = fastjsonschema.compile(
            dynamic_schema, handlers={"http": fetch_schema, "https": fetch_schema}
        )
    except Exception:
        # FALLBACK: Some schemas (like Item Assets) cause fastjsonschema to generate invalid python code.
        # We fall back to the standard jsonschema library.
        click.secho(
            "    [Fallback] fastjsonschema compile failed. Using python-jsonschema.",
            fg="yellow",
            dim=True,
        )
        import jsonschema

        # Create a validator using the same custom logic
        def fallback_validator(data: Dict[str, Any]) -> None:
            # We need a resolver to handle the remote $refs
            resolver = jsonschema.RefResolver(
                base_uri="",
                referrer=dynamic_schema,
                handlers={"http": fetch_schema, "https": fetch_schema},
            )
            jsonschema.validate(data, dynamic_schema, resolver=resolver)

        validator = fallback_validator

    VALIDATOR_CACHE[cache_key] = validator
    return validator, False


class FastValidator:
    def __init__(self, stac_file: str, quiet: bool = False, verbose: bool = False):
        global QUIET_MODE
        self.stac_file = stac_file
        self.quiet = quiet
        self.valid = True
        self.verbose = verbose
        self.message: List[Dict[str, Any]] = []
        QUIET_MODE = quiet

    def run(self):
        """Universal high-speed STAC Validator (Items, Collections, Catalogs, FeatureCollections)"""
        if not self.quiet:
            click.secho(f"\n📂 Loading: {self.stac_file}", fg="blue", bold=True)

        try:
            if self.stac_file.startswith("http"):
                req = urllib.request.Request(
                    self.stac_file, headers={"User-Agent": "stac-fast-cli/5.0"}
                )
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode("utf-8"))
            else:
                with open(self.stac_file, "r") as f:
                    data = json.load(f)
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
            stac_type_lower = actual_type.lower()
            if stac_type_lower in ["item", "feature"]:
                base_schema = f"https://schemas.stacspec.org/v{stac_version}/item-spec/json-schema/item.json"
            elif stac_type_lower == "collection":
                base_schema = f"https://schemas.stacspec.org/v{stac_version}/collection-spec/json-schema/collection.json"
            elif stac_type_lower == "catalog":
                base_schema = f"https://schemas.stacspec.org/v{stac_version}/catalog-spec/json-schema/catalog.json"
            else:
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
                continue
            t1 = time.perf_counter()
            setup_time = (t1 - t0) * 1000
            total_setup_ms += setup_time

            # --- Execution Timer ---
            t2 = time.perf_counter()
            try:
                validator(item)
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

    def run_recursive(self):
        """Recursively validate a local STAC catalog/collection and all its children."""
        import json

        sys.setrecursionlimit(10000)

        # Load the root STAC object
        try:
            if self.stac_file.startswith("http"):
                req = urllib.request.Request(
                    self.stac_file, headers={"User-Agent": "stac-fast-cli/5.0"}
                )
                with urllib.request.urlopen(req) as response:
                    root_data = json.loads(response.read().decode("utf-8"))
                root_path = self.stac_file
            else:
                with open(self.stac_file, "r") as f:
                    root_data = json.load(f)
                root_path = os.path.abspath(self.stac_file)
        except Exception as e:
            click.secho(f"❌ Error reading {self.stac_file}: {e}", fg="red", bold=True)
            self.valid = False
            return

        # Recursively validate the root and all children
        results = []
        visited = set()
        visited.add(root_path)
        self._validate_recursive(root_data, root_path, results, visited, is_api=False)

        # Display results
        click.echo("\n" + "=" * 55)
        click.secho("📊 RECURSIVE VALIDATION SUMMARY", bold=True, fg="blue")
        click.echo("=" * 55)

        valid_count = sum(1 for r in results if r["valid_stac"])
        invalid_count = len(results) - valid_count

        click.echo(f"Total Objects Validated: {len(results)}")
        click.echo(f"Valid Objects:           {valid_count}")
        click.echo(f"Invalid Objects:         {invalid_count}")

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
        self.valid = invalid_count == 0
        self.message = results

    def run_api(self):
        """Recursively validate a STAC API catalog and all its collections/items."""
        import json

        sys.setrecursionlimit(10000)

        if not self.quiet:
            click.secho("🚀 Starting STAC API validation...", fg="blue", bold=True)

        # Load the root STAC API object
        try:
            if self.stac_file.startswith("http"):
                req = urllib.request.Request(
                    self.stac_file, headers={"User-Agent": "stac-fast-cli/5.0"}
                )
                with urllib.request.urlopen(req) as response:
                    root_data = json.loads(response.read().decode("utf-8"))
                root_path = self.stac_file
            else:
                with open(self.stac_file, "r") as f:
                    root_data = json.load(f)
                root_path = os.path.abspath(self.stac_file)
        except Exception as e:
            click.secho(f"❌ Error reading {self.stac_file}: {e}", fg="red", bold=True)
            self.valid = False
            return

        # Recursively validate the root and all children (API mode)
        results = []
        visited = set()
        visited.add(root_path)
        # Add a counter for progress tracking
        self._progress_count = 0
        self._validate_recursive(root_data, root_path, results, visited, is_api=True)

        # Display results
        click.echo("\n" + "=" * 55)
        click.secho("📊 STAC API VALIDATION SUMMARY", bold=True, fg="blue")
        click.echo("=" * 55)

        valid_count = sum(1 for r in results if r["valid_stac"])
        invalid_count = len(results) - valid_count

        click.echo(f"Total Objects Validated: {len(results)}")
        click.echo(f"Valid Objects:           {valid_count}")
        click.echo(f"Invalid Objects:         {invalid_count}")

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
        self.valid = invalid_count == 0
        self.message = results

    def _validate_recursive(
        self,
        data: Dict[str, Any],
        file_path: str,
        results: List[Dict],
        visited: Set[str],
        is_api: bool = False,
        collection_id: str = None,
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
        import json

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

                # Mute noisy "[Fallback]" and "[Network]" prints from validator setup
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    validator, _ = get_validator(stac_type, stac_version, extensions)
                    validator(data)

                is_valid = True
                error_msg = None
            except fastjsonschema.JsonSchemaValueException as e:
                is_valid = False
                error_msg = f"{e.name} {e.message.replace(e.name, '').strip()}"
            except Exception as e:
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

        # Process child links
        base_dir = (
            os.path.dirname(file_path)
            if not file_path.startswith("http")
            else file_path.rsplit("/", 1)[0]
        )
        links = data.get("links", [])

        for link in links:
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
                    if child_path.startswith("http"):
                        req = urllib.request.Request(
                            child_path, headers={"User-Agent": "stac-fast-cli/5.0"}
                        )
                        with urllib.request.urlopen(req) as response:
                            child_data = json.loads(response.read().decode("utf-8"))
                    else:
                        with open(child_path, "r") as f:
                            child_data = json.load(f)

                    # If this is a collections list endpoint, extract individual collections
                    if rel == "data" and is_api and isinstance(child_data, dict):
                        collections = child_data.get("collections", [])
                        if collections:
                            # This is a collections list - process each collection
                            for collection in collections:
                                collection_id = collection.get("id")
                                if collection_id:
                                    # Build URL to individual collection
                                    collection_url = (
                                        f"{child_path.rstrip('/')}/{collection_id}"
                                    )
                                    try:
                                        req = urllib.request.Request(
                                            collection_url,
                                            headers={"User-Agent": "stac-fast-cli/5.0"},
                                        )
                                        with urllib.request.urlopen(req) as response:
                                            collection_data = json.loads(
                                                response.read().decode("utf-8")
                                            )
                                        # Recursively validate the full collection
                                        self._validate_recursive(
                                            collection_data,
                                            collection_url,
                                            results,
                                            visited,
                                            is_api,
                                        )
                                    except Exception as e:
                                        results.append(
                                            {
                                                "path": collection_url,
                                                "valid_stac": False,
                                                "error_message": f"Failed to load: {str(e)}",
                                            }
                                        )
                        else:
                            # Not a collections list, validate as normal
                            self._validate_recursive(
                                child_data, child_path, results, visited, is_api
                            )
                    # If this is an items endpoint (GeoJSON FeatureCollection), extract individual items
                    elif rel == "items" and is_api and isinstance(child_data, dict):
                        features = child_data.get("features", [])
                        if features:
                            # Extract collection ID from URL (e.g., /collections/{id}/items)
                            collection_id = None
                            if "/collections/" in child_path:
                                parts = child_path.split("/collections/")
                                if len(parts) > 1:
                                    collection_parts = parts[1].split("/items")
                                    collection_id = (
                                        collection_parts[0]
                                        if collection_parts
                                        else None
                                    )

                            # This is an items list - process each item
                            for feature in features:
                                item_id = feature.get("id", "unknown")
                                item_path = f"{child_path}#{item_id}"
                                self._validate_recursive(
                                    feature,
                                    item_path,
                                    results,
                                    visited,
                                    is_api,
                                    collection_id,
                                )
                        else:
                            # Not an items list, validate as normal
                            self._validate_recursive(
                                child_data, child_path, results, visited, is_api
                            )
                    else:
                        # Recursively validate child
                        self._validate_recursive(
                            child_data, child_path, results, visited, is_api
                        )
                except Exception as e:
                    results.append(
                        {
                            "path": child_path,
                            "valid_stac": False,
                            "error_message": f"Failed to load: {str(e)}",
                        }
                    )
