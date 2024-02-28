from io import BytesIO
import base64
import json
from PIL import Image

from utils import parse_list, merge_identical_boxes,select_best_from_identical_boxes,merge_parsed_list
from assemble import construct_spec, clean_track_info
from object_detection import predict


def add_title(e):
    e[1]["title"] = str(e[0]+1)
    return e[1]

def rank_tracks(tracks):
    return list(sorted(tracks,key=lambda el: (el['x'], el['y'])))

def pil2datauri(img):
    #converts PIL image to datauri
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8')

def viz_analysis(image):
    pil_image = Image.open(image)
    if not pil_image.mode == 'RGB':
        pil_image = pil_image.convert('RGB')
    
    # Resize the image
    width, height = pil_image.size
    new_width = 600
    new_height = int((new_width / width) * height)
    pil_image = pil_image.resize((new_width, new_height))
    
    shape_img, _, shape_info, prop_info = predict(pil_image)

    '''
    Example format: EX_TRACK_INFO = [
        {'x': 0, 'y': 0, 'width': 400, 'height': 430, 'layout': 'linear', 'mark': 'bar'}, 
        {'x': 0, 'y': 450, 'width': 400, 'height': 430, 'layout': 'linear', 'mark': 'line'}, 
        {'x': 410, 'y': 0, 'width': 400, 'height': 880, 'layout': 'linear', 'mark': 'point'}, 
        {'x': 0, 'y': 890, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': 'area'}, 
        {'x': 0, 'y': 1100, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': 'line'}]
    '''

    shape_info_parsed = select_best_from_identical_boxes([parse_list(my_list) for my_list in shape_info])


    prop_info_parsed = merge_identical_boxes([parse_list(my_list) for my_list in prop_info])


    def add_orientation(info):
        new_obj = info.copy()
        orientation_set = {"horizontal","vertical"}
        new_obj['orientation'] = [el for el in info['mark'] if el in orientation_set]
        if len(new_obj['orientation']) == 0:
            new_obj['orientation'] = ['horizontal']
        new_obj['mark'] = [el for el in info['mark'] if el not in orientation_set]
        return new_obj
    raw_tracks_info = merge_parsed_list(shape_info_parsed,prop_info_parsed)

    tracks_info = [add_orientation(info) for info in raw_tracks_info]
    tracks_info = [track_info for track_info in tracks_info if len(track_info['mark']) > 0]
    tracks_info = rank_tracks(tracks_info)

    # '''
    # images = {
    #     "image" : shape_img,
    # }
    # response = {key:pil2datauri(val) for key, val in images.items()}
    response = {}
    
    width, height = shape_img.size

    if len(tracks_info) > 0:
        tracks_info = list(map(clean_track_info, tracks_info))
        tracks_info = sorted(tracks_info, key=lambda x: (x["y"],x["x"],))
        with_title_tracks_info = list(map(add_title, enumerate(tracks_info)))
        temp_spec = construct_spec(with_title_tracks_info,"vertical")
        if "views" not in temp_spec:
            temp_spec = {"views": [temp_spec]}
        response["spec"] = temp_spec 

    response["tracks_info"]= tracks_info
    response["width"] = width
    response["height"] = height
    return response["spec"]

if __name__ == "__main__":
    import sys
    image_path = sys.argv[1]
    response = viz_analysis(image_path)
    print(json.dumps(response, indent=2))