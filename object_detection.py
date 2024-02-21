import cv2
import onnxruntime as ort
from PIL import Image, ImageColor, ImageDraw
import numpy as np

cuda = True
w = "best.onnx"

providers = ['CPUExecutionProvider']
session = ort.InferenceSession(w, providers=providers)

def letterbox(im, new_shape=(640, 640), color=(0, 0, 0), auto=True, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    # import ipdb; ipdb.set_trace()
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)

classes = ["area", "bar", "betweenLink", "circular", "heatmap", "horizontal", "ideogram", "line", "linear", "point", "rect", "rule", "text", "triangleLeft", "triangleRight", "vertical", "withinLink"]
colors = {name : ImageColor.getrgb(f'hsv({int(360 * i / len(classes))},100%,100%)') for i, name in enumerate(classes)}

def predict(img):
  image = np.array(img.copy())
  img = np.array(img.copy())
  image, ratio, dwdh = letterbox(image, auto=False)
  image = image.transpose((2, 0, 1))
  image = np.expand_dims(image, 0)
  image = np.ascontiguousarray(image)

  im = image.astype(np.float32)
  im /= 255

  outname = [i.name for i in session.get_outputs()]
  inname = [i.name for i in session.get_inputs()]

  inp = {inname[0]:im}
  outputs = session.run(outname, inp)[0]

  def make_image(class_set):
    important_info = []
    ori_images = [img.copy()]
    for i,(batch_id,x0,y0,x1,y1,cls_id,score) in enumerate(outputs):
        image = ori_images[int(batch_id)]
        box = np.array([x0,y0,x1,y1])
        box -= np.array(dwdh*2)
        box /= ratio
        box = box.round().astype(np.int32).tolist()
        cls_id = int(cls_id)
        score = round(float(score),3)
        name = classes[cls_id]
        color = colors[name]
        if name in class_set:
            name += ' '+str(score)
            new_x0, new_y0, new_x1, new_y1 = box
            important_info.append((classes[cls_id],new_x0,new_y0,new_x1,new_y1,cls_id,score))
    return Image.fromarray(ori_images[0]), important_info
  
  shape_image, shape_info = make_image(["linear","circular"])
  other_image, other_info = make_image([el for el in classes if el not in ['linear','circular']])

  return shape_image, other_image, shape_info, other_info


def draw_bounding_boxes(im: Image, bboxes: np.ndarray, classes: np.ndarray,
                        scores: np.ndarray) -> Image:
    im = im.copy()
    num_classes = len(set(classes))
    class_to_color_id = {cls: i for i, cls in enumerate(set(classes))}

    colors = [ImageColor.getrgb(f'hsv({int(360 * x / num_classes)},100%,100%)') for x in range(num_classes)]

    draw = ImageDraw.Draw(im)

    for bbox, cls, score in zip(bboxes, classes, scores):
        color = colors[class_to_color_id[cls]]
        draw.rectangle((*bbox.astype(np.int64),), outline=color)

        text = f'{cls}: {int(100 * score)}%'
        text_w, text_h = draw.textsize(text)
        draw.rectangle((bbox[0], bbox[1], bbox[0] + text_w, bbox[1] + text_h), fill=color, outline=color)
        draw.text((bbox[0], bbox[1]), text, fill=(0, 0, 0))

    return im