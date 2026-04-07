#!/usr/bin/env python3

# Test just the API logic without Flask
import requests
import base64

print("Testing Picsart API directly...")

# Test data
test_prompt = "A realistic portrait of a young woman with brown hair, smiling"
print(f"Test prompt: {test_prompt}")

# Picsart API Configuration
PICSART_API_KEY = 'paat-cnwt9YRGEVCr7TJybU8rNhynojl'

url = "https://genai-api.picsart.io/v1/text2image"

payload = {
    "width": 1024,
    "height": 1024,
    "count": 1,
    "model": "urn:air:sdxl:model:fluxai:flux_kontext_max@1"
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-Picsart-API-Key": PICSART_API_KEY
}

print("Sending request to Picsart API...")
response = requests.post(url, json=payload, headers=headers)

print(f"Response Status: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")
print(f"Response Content: {response.text[:500]}...")

if response.status_code == 200:
    result = response.json()
    print(f"Parsed JSON: {result}")
    
    if 'data' in result and len(result['data']) > 0:
        image_url = result['data'][0]['url']
        print(f"Image URL: {image_url}")
        
        # Download the image
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            image_bytes = img_response.content
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            print(f"✅ Success! Generated image ({len(image_bytes)} bytes)")
            print(f"Base64 length: {len(image_base64)} characters")
        else:
            print(f"❌ Failed to download image: {img_response.status_code}")
    else:
        print(f"❌ No image data in response")
else:
    print(f"❌ API Error: {response.status_code}")
    print(f"Error details: {response.text}")
