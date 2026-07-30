#!/usr/bin/env python3
"""
Test script for get_validator function with storage extension.
"""

import json
from stac_validator.fast_validator import get_validator

# Load test item with storage extension
with open("test.json", "r") as f:
    item = json.load(f)

# Get extensions from item
extensions = item.get("stac_extensions", [])
stac_version = item.get("stac_version", "1.1.0")
stac_type = item.get("type", "Feature")

print("=" * 70)
print(f"Testing get_validator with {len(extensions)} extensions")
print(f"STAC Type: {stac_type}, Version: {stac_version}")
print("=" * 70)
print()

# Get the validator
validator, cached = get_validator(stac_type, stac_version, extensions)

print(f"Validator obtained (cached={cached})")
print()

# Test validation
try:
    validator(item)
    print("✅ Validation passed!")
except Exception as e:
    print(f"❌ Validation failed: {e}")
print()

print("=" * 70)
print("Test completed!")
print("=" * 70)
