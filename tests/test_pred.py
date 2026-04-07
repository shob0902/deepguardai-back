import sys
import requests

if len(sys.argv) < 2:
    print('Usage: python test_pred.py PATH_TO_IMAGE')
    sys.exit(1)

img_path = sys.argv[1]
url = 'http://127.0.0.1:5000/predict'

with open(img_path, 'rb') as f:
    try:
        r = requests.post(url, files={'image': f})
    except requests.exceptions.RequestException as e:
        print('Request failed:', e)
        sys.exit(2)

print('Status:', r.status_code)
try:
    print(r.json())
except Exception:
    print(r.text)
