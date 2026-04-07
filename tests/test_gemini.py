#!/usr/bin/env python3

# Test script for Gemini API setup
import sys

print("Testing Gemini API setup...")

# Test imports
try:
    import google.generativeai as genai
    print("✓ Google Generative AI imported successfully")
except ImportError as e:
    print(f"✗ Google Generative AI import failed: {e}")
    sys.exit(1)

try:
    import requests
    print("✓ Requests imported successfully")
except ImportError as e:
    print(f"✗ Requests import failed: {e}")
    sys.exit(1)

try:
    import base64
    print("✓ Base64 imported successfully")
except ImportError as e:
    print(f"✗ Base64 import failed: {e}")
    sys.exit(1)

# Test Gemini API configuration
try:
    GEMINI_API_KEY = 'AIzaSyAkEhZj1P46P-nCjZuCES8dJIm4IgCiw3Y'
    genai.configure(api_key=GEMINI_API_KEY)
    print("✓ Gemini API configured successfully")
except Exception as e:
    print(f"✗ Gemini API configuration failed: {e}")
    sys.exit(1)

# Test Gemini model initialization
try:
    model = genai.GenerativeModel('gemini-pro')
    print("✓ Gemini Pro model initialized successfully")
except Exception as e:
    print(f"✗ Gemini model initialization failed: {e}")
    sys.exit(1)

print("\n✓ All Gemini API setup working!")
print("Note: Gemini Pro is for text generation, not image generation.")
print("For image generation, you would need:")
print("1. OpenAI DALL-E API")
print("2. Stability AI API") 
print("3. Or another dedicated image generation service")
