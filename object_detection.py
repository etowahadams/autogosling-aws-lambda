import onnxruntime as ort
from PIL import Image, ImageColor, ImageDraw
import numpy as np

cuda = True
w = "best.onnx"

providers = ['CPUExecutionProvider']
session = ort.InferenceSession(w, providers=providers)

classes = ["area", "bar", "betweenLink", "circular", "heatmap", "horizontal", "ideogram", "line", "linear", "point", "rect", "rule", "text", "triangleLeft", "triangleRight", "vertical", "withinLink"]
colors = {name : ImageColor.getrgb(f'hsv({int(360 * i / len(classes))},100%,100%)') for i, name in enumerate(classes)}

def prepare_image(image: Image.Image, size: int) -> np.ndarray:
    # Get original image dimensions
    w, h = image.size
    
    # Calculate aspect ratio
    ratio = min(size / w, size / h)

    # Calculate new dimensions
    dw, dh = int(w * ratio), int(h * ratio)

    # Resize image
    resized_image = image.resize((dw, dh))

    # Create a new blank image canvas
    canvas = Image.new('RGB', (size, size), (255, 255, 255))

    # Calculate paste position
    paste_x = (size - dw) // 2
    paste_y = (size - dh) // 2

    # Paste resized image onto the canvas
    canvas.paste(resized_image, (paste_x, paste_y))

    return np.array(canvas), ratio, (w - dw, h - dh)

def predict(pil_img: Image.Image):
  image = np.array(pil_img.copy())
  np_img = np.array(pil_img.copy())
  
  image, ratio, dwdh = prepare_image(pil_img, 640)
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
    ori_images = [np_img.copy()]
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