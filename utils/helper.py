import numpy as np
import cv2
import json
import os


def load_image(data):
    """
    Load image from request.data object
    :param data: request.data object
    :return: numpy, grayscale image
    """
    image_array = np.fromstring(data, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


def main(thread):
    """
    Start logo and OCR services in different cores
    :param thread: linux bash script
    :return: None
    """
    os.system(thread)
