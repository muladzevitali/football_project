from flask import Flask, request, jsonify
from waitress import serve
import os
from api.utils import send_request
from utils.ocr.utils.ocr_utils import (get_names)
from utils.ocr.utils.flags import init_character_config
from utils.detection.yolo.utils.loader import load_model
import cv2
import numpy
import torch
from utils.detection.yolo.yolo.preprocess import prep_image
from utils.detection.yolo.utils.detector import detection
from utils.ocr.utils.resnet import resnet18
from utils.ocr.ocr_resnet import preprocess_image, get_letter_from_index
import time
from configuration import Options, Config

_OK = 'ok'
_NO_IMG_WARNING = 'Image was not found'
_NO_TEXT_WARNING = 'Text was not found'

app = Flask(__name__)

if not os.path.isdir('data/ocr/characters'):
    os.mkdir('data/ocr/characters')


def character_localization(image, model):
    """
    Localize characters in text image
    :param image: numpy array -- image
    :param model: detector object -- yolo detector
    :return: localized characters bboxes as list or -1
    """
    image_loader = prep_image(image, height, path=False)
    results = detection(image_loader, model, flags, draw=False)

    return results if results else -1


def character_recognition(characters_list, image, model):
    """
    Recognize characters from image bboxes
    :param characters_list: list -- characters bboxes
    :param image: numpy array -- image
    :param model: resnet object -- resnet model
    :return: recognized text or -1
    """
    recognized_text = ''
    for character in sorted(characters_list, key=lambda x: x[0][0]):
        top_left, bottom_right = character[0:2]
        cropped_image = image[top_left[1]:bottom_right[1], top_left[0]: bottom_right[0]]
        character = preprocess_image(cropped_image)
        if Config.save_outputs:
            cv2.imwrite(f'data/ocr/characters/_{str(time.time()).split(".")[0]}.jpg', cropped_image)

        with torch.no_grad():
            output = model(character)
            output = numpy.array(output)
            index = numpy.argmax(output)

            recognized_text += get_letter_from_index(index)

    return recognized_text.upper() if recognized_text else -1


@app.route('/', methods=['GET', 'POST'])
def read_text():
    if request.data:
        # Preprocess image
        image_array = numpy.fromstring(request.data, numpy.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Get characters coordinates detected from yolo as list
        localized_characters = character_localization(image, yolo_model)

        # If yolo detected any characters
        if type(localized_characters) is list:

            # Get characters as word from resnet
            recognized_text = character_recognition(localized_characters, image, resnet_model)

            # Dump recognized texts
            if Config.save_outputs:
                with open('data/ocr/detected.txt', 'a') as output_file:
                    output_file.write(recognized_text + '\n')

            # If no characters classified
            if type(recognized_text) is int:
                return jsonify(_NO_TEXT_WARNING)

            # If Classified word is not in allowed words:
            elif not NAMES.get(recognized_text):
                return jsonify(_NO_IMG_WARNING)

            else:
                # Return detected word
                result_json = {'info': recognized_text, 'time': request.headers['time'],
                               'source': 'Text', 'user': request.headers['user'],
                               'vidname': request.headers['vidname']}
                send_request('http://127.0.0.1:{}/player/objects'.format(Config.detection_service_port),
                             headers=result_json)
                return jsonify(_OK)
        else:
            return jsonify(_NO_IMG_WARNING)
    else:
        return jsonify(_NO_IMG_WARNING)


if __name__ == "__main__":
    # Initialize model details
    flags = init_character_config()

    # Initialize yolo model
    yolo_model = load_model(flags)
    height = yolo_model.net_info['height']

    # Get allowed names dictionary
    NAMES = get_names('utils/ocr/names')

    # Initialize resnet model
    resnet_model = resnet18(pretrained=True)

    if torch.cuda.is_available():
        resnet_model.load_state_dict(torch.load('utils/ocr/models/character-recognition-gpu'))
    else:
        resnet_model.load_state_dict(torch.load('utils/ocr/models/character-recognition-cpu'))

    resnet_model.eval()
    # Start service
    serve(app.wsgi_app, port=Options.ocr_service_port, threads=True, connection_limit=10000, asyncore_use_poll=True)
