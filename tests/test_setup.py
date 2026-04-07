#!/usr/bin/env python3

# Test basic imports
print("Testing basic imports...")

try:
    import flask
    print("✅ Flask imported")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")

try:
    import requests
    print("✅ Requests imported")
except ImportError as e:
    print(f"❌ Requests import failed: {e}")

try:
    import base64
    print("✅ Base64 imported")
except ImportError as e:
    print(f"❌ Base64 import failed: {e}")

try:
    import os
    print("✅ OS imported")
except ImportError as e:
    print(f"❌ OS import failed: {e}")

try:
    import google.generativeai
    print("✅ Google Generative AI imported")
except ImportError as e:
    print(f"❌ Google Generative AI import failed: {e}")

print("\n✅ All imports successful!")
print("Environment is ready for Flask app")
