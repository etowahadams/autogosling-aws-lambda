import json
import base64
from io import BytesIO
from main import viz_analysis

def main(event, context):

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