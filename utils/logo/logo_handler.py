import os
import json
from utils.logo.cnn.search.cnn_files import files as _files
import faiss
import numpy
from utils.logo.cnn.search.features_extractor import extract_embedding
import cv2
from PIL import Image


def dump_json(dict_file, index, flags):
    dict_path = _files.data_file(flags.dict_path)
    index_path = _files.data_file(flags.index_path)

    faiss.write_index(index, index_path)
    with open(dict_path, 'w') as file:
        json.dump(dict_file, file)


def get_links_dict(input_file):
    """
    Get inputs mapper in dictionary
    :param input_file: dict_file
    :return: inputs mapper dictionary
    """
    links_path = _files.data_file(input_file)

    if os.path.exists(links_path):
        with open(links_path, 'r') as file:
            links_dict = json.loads(file.read())
    else:
        links_dict = dict()
    return links_dict


def extract_features(model, preprocessors, data=None, image_path=None):
    if image_path:
        image_numpy = cv2.imread(image_path)
    else:
        image_array = numpy.fromstring(data, numpy.uint8)
        image_numpy = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    image = Image.fromarray(image_numpy, 'RGB')
    features_var = extract_embedding(model, preprocessors, image)
    features_vector = features_var.data.numpy()
    return features_vector, image_numpy


def rename_logos(team, folder):
    """
    Rename images for inserting in faiss
    :param team: string -- team name as in mapper.json
    :param folder: sting -- folder path
    :return: None
    """
    for image in os.listdir(folder):
        if image[0] == '_':
            image_path = os.path.join(folder, image)
            new_path = os.path.join(folder, team + image)
            os.rename(image_path, new_path)
