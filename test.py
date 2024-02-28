import requests
import base64

IMG_PATH = './glyph.png'
API_URL = ''

# encode image to b64
with open(IMG_PATH, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode('ascii')


# trigger api
result = requests.get(API_URL, json={"image": img_b64})
print(result.json()['spec'])

