from io import BytesIO
import base64
import json
from PIL import Image

from main import viz_analysis

def handler(event, context):
    try:
        body = json.loads(event['body'])
        img_b64 = body['image']
        img = BytesIO(base64.b64decode(img_b64.encode('ascii')))

        spec = viz_analysis(img)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "spec": spec
            }),
        }
    except:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal server error"
            }),
        }