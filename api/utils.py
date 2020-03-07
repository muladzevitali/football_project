import os
import time

import cv2
import requests

from configuration import Config

_OK = 'ok'


def list_files(folder):
    """
    :param folder:
    :return:
    """
    f_str = ""
    for f in os.listdir(folder):
        f_str += "<option>" + f + "</option>\r\n"
    return f_str


def allowed_file(filename, allowed):
    """
    Check if filename in allowed extensions
    :param filename: string -- file name
    :param allowed: list -- allowed types list
    :return: bool
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in allowed


def send_request(url, headers, data=None):
    """
    Send request to url without waiting for response
    :param url: string -- url of server
    :param headers: dictionary -- info for header in request
    :param data: string -- encoded in string image
    :return: None
    """
    try:
        if data:
            requests.post(url, data=data, headers=headers, timeout=0.0001)
        else:
            requests.post(url, headers=headers, timeout=0.0001)
    except requests.exceptions.ReadTimeout:
        pass


def handle_results(frame, results, labels, user, vidname, r_time, detect_text, detect_logos):
    folder_name = vidname.split('/')[1].split('.')[0].upper()
    headers = {'time': str(r_time), 'user': user, "vidname": vidname, "folder_name": folder_name}

    for result in results:
        top_left, bottom_right = result[0:2]
        label = labels[result[2]]
        cropped_image = frame[top_left[1]:bottom_right[1], top_left[0]: bottom_right[0]]
        if not cropped_image.any():
            continue
        _, img_encoded = cv2.imencode('.jpg', cropped_image)

        if label == 'TEXT' and detect_text == "true":
            if Config.save_text_images:
                cv2.imwrite(f'data/ocr/unlabeled/{folder_name}/_{str(time.time()).split(".")[0]}.jpg', cropped_image)
            # Send request straight to detection for now
            res = {'info': "No more information", 'time': headers['time'],
                   'source': 'Text', 'user': headers['user'], 'vidname': headers['vidname']}
            send_request('http://127.0.0.1:{}/player/objects'.format(Config.detection_service_port), headers=res)
            # Send to ocr-service.py
            send_request('http://127.0.0.1:{}/'.format(Config.ocr_service_port), headers, data=img_encoded.tostring())

            frame = cv2.rectangle(frame, top_left, bottom_right, (89, 229, 165), 2)
            frame = cv2.rectangle(frame, top_left, (top_left[0] + 50, top_left[1] - 20), (89, 229, 165), -1)
            frame = cv2.putText(frame, label, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (62, 62, 62), 2)
            pass

        if label == 'LOGO' and detect_logos == "true":
            headers["folder_name"] = folder_name
            send_request('http://127.0.0.1:{}/'.format(Config.logo_service_port), headers, data=img_encoded.tostring())

            frame = cv2.rectangle(frame, top_left, bottom_right, (89, 229, 165), 2)
            frame = cv2.rectangle(frame, top_left, (top_left[0] + 60, top_left[1] - 20), (89, 229, 165), -1)
            frame = cv2.putText(frame, label, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (62, 62, 62), 2)
    return frame
