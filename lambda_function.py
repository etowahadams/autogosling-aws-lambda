from io import BytesIO
import base64
import json
from PIL import Image

from utils import parse_list, merge_identical_boxes,select_best_from_identical_boxes,merge_parsed_list
from assemble import construct_spec, clean_track_info

import onnxruntime as ort
from PIL import Image, ImageColor, ImageDraw
import numpy as np

def handler(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world"
        }),
    }

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