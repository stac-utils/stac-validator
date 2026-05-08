import json
import sys

import requests


def test_validate_collection(
    file_path: str, server_url: str = "http://localhost:8000/validate"
):
    """Sends a local STAC file to the validation server and prints the result."""

    # 1. Load the ItemCollection
    try:
        with open(file_path, "r") as f:
            stac_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File {file_path} not found.")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: File {file_path} is not valid JSON.")
        return

    print(f"🚀 Sending '{file_path}' to {server_url}...")

    # 2. POST to the server
    try:
        response = requests.post(server_url, json=stac_data)

        # Check if the server returned an error (e.g., 500 or 422)
        if response.status_code != 200:
            print(f"❌ Server Error ({response.status_code}): {response.text}")
            return

        result = response.json()

        # Double check the expected keys exist before trying to print them
        if "valid_stac" not in result:
            print(f"❌ Error: Server response format unexpected: {result}")
            return

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request failed: {e}")
        return

    # 3. Print the formatted result
    print("\n" + "=" * 50)
    print("📊 API VALIDATION RESULT")
    print("=" * 50)
    # Corrected key: valid_stac
    status_text = "✅ VALID" if result.get("valid_stac") else "❌ INVALID"
    print(f"Status          : {status_text}")
    print(f"Total Objects   : {result.get('total_objects')}")
    print(f"Valid Objects   : {result.get('valid_objects')}")
    print(f"Invalid Objects : {result.get('invalid_objects')}")
    print(f"Execution Time  : {result.get('execution_time_ms', 0):.2f} ms")
    print("-" * 50)

    # Corrected keys: errors, error_message, affected_items
    if result.get("errors"):
        print("🚨 ERRORS FOUND:")
        for err in result["errors"]:
            msg = err.get("error_message", "Unknown Error")
            count = err.get("count", 0)
            samples = ", ".join(err.get("affected_items", [])[:3])
            print(f"- [{count} objects] {msg}")
            print(f"  Examples: {samples}")

    print("=" * 50 + "\n")

    print(
        "result dict:", json.dumps(result, indent=2)
    )  # Debug: Print the full result dict


if __name__ == "__main__":
    # Defaulting to your sample collection if no argument provided
    target_file = (
        sys.argv[1] if len(sys.argv) > 1 else "sample_data/sentinel-cogs_0_100.json"
    )
    test_validate_collection(target_file)
