import requests
import os
from configuration import Options

_UNLABELED_LOGOS = 'data/logo/unlabeled'
_LABELED_LOGOS = 'data/logo/labeled'
_OK = 'OK'


def insert_logo(_form):

    image_name = list(_form.keys())[0]
    company = _form[image_name].replace(' ', '-')
    if not company:
        return None
    image_path = os.path.join(_UNLABELED_LOGOS, image_name)
    headers = {'path': image_path, 'company': company}
    response = requests.post(f'http://127.0.0.1:{Options.logo_service_port}/insert', headers=headers)
    features_vector, image_id = response.json()

    new_name = company + '_' + image_name
    headers.update({'vector': features_vector, 'id': image_id, 'path': new_name})
    os.rename(image_path, os.path.join(_LABELED_LOGOS, new_name.replace("/", "_")))

    return headers


def insert_logos_multiple(_form):
    company_name = _form.get("choose_box").replace(" ", "-")
    if not company_name:
        return
    logos_list = list()
    for image_name in _form:
        if image_name == "choose_box":
            continue
        image_path = os.path.join(_UNLABELED_LOGOS, image_name)
        headers = {'path': image_path, 'company': company_name}
        response = requests.post(f'http://127.0.0.1:{Options.logo_service_port}/insert', headers=headers)
        features_vector, image_id = response.json()
        new_name = company_name + '_' + image_name
        headers.update({'vector': features_vector, 'id': image_id, 'path': new_name})
        logos_list.append(headers)
        os.rename(image_path, os.path.join(_LABELED_LOGOS, new_name.replace("/", "_")))

    return logos_list