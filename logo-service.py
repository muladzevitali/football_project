from flask import request, jsonify
from waitress import serve

from api.resources.logos import LogosMapper
from api.utils import *
from configuration import Options
from utils.logo.app import app
from utils.logo.cnn.search.input_utils import init_transforms
from utils.logo.cnn.search.network_models import init_model
from utils.logo.cnn.search.training_flags import init_default_config
from utils.logo.logo_handler import (dump_json, extract_features)
from utils.logo.vector_database import (init_db, insert_vector_and_id, find_vector)

_NO_IMG_WARNING = 'Image was not uploaded'
_IMG_ALREADY_EXIST = 'Image already exists'


def insert(image_path, company):
    """
    Insert image in faiss database and save image path
    :param company:
    :param image_path: string -- full path of the image
    :return: 'ok' if it insertion success
    """
    # Extract features vector from image
    features_vector, _ = extract_features(model, preprocessors, data=None, image_path=image_path)
    # Number of vectors in faiss database
    image_id = index.ntotal
    # Insert features vector in faiss database at the place image_id i.e last place
    _ = insert_vector_and_id(image_id, features_vector, index)
    # Insert image path and its corresponding place in faiss in input mapper
    vectors_dict[str(image_id)] = company
    # Update faiss index and input mapper
    dump_json(vectors_dict, index, flags)
    # Jsonify the result, 'ok' if success
    result_json = jsonify([features_vector[0].tolist(), image_id])

    return result_json


@app.route('/insert', methods=['POST'])
def insert_nn():
    """
    Insertion route for image
    :return: 'ok' if success else No image warning
    """
    # Get image path from request
    image_path = request.headers['path']
    company = request.headers['company']
    if image_path:
        # Insert path to faiss database if request was correct
        result_json = insert(image_path, company)
    else:
        # Return No image warning
        result_json = jsonify(_NO_IMG_WARNING)

    return result_json


@app.route('/', methods=['POST'])
def search_nn():
    """
    Search route for image
    :return: result json
    """
    # Get image from requests
    data = request.data
    folder = request.headers.get("Vidname", None)
    if folder:
        folder = folder.split("/")[-1].split(".")[0].upper()
    else:
        folder = 'UNKNOWN'
    os.makedirs(f"data/logo/unlabeled/{folder}", exist_ok=True)
    if data:
        # Get features vector from image
        features_vector, image = extract_features(model, preprocessors, data=data, image_path=None)
        # Search nearest neighbours in faiss database
        search_result, distance = find_vector(features_vector, n_results=flags.n_results, index_faiss=index)
        # Search corresponding logo in input mapper
        nearest_logo = vectors_dict[str(search_result)]
        # Get name of search logo
        searched_logo = nearest_logo.split('/')[-1].split('_')[0]
        if Options.log_logos_service:
            print(f'Searched logo: {searched_logo.encode("utf-8")}, distance: {distance}')
            app.logger.info(f'Searched logo: {searched_logo.encode("utf-8")}, distance: {distance}')
        # Get result if distance is smaller than 150
        if distance < 500:
            result_json = {'info': searched_logo, 'time': request.headers['time'],
                           'source': 'Logo', 'user': request.headers['user'], 'vidname': request.headers['vidname']}
            send_request('http://127.0.0.1:{}/player/objects'.format(Config.detection_service_port), headers=result_json)
            result_json = jsonify(result_json)
        else:
            if Options.save_logos:
                if Options.log_logos_service:
                    print(f'Searched logo: {searched_logo.encode("utf-8")}, distance: {distance}')
                    app.logger.info('Not found')
                cv2.imwrite(f'data/logo/unlabeled/{folder}/_{str(time.time()).split(".")[0]}.jpg', image)
            result_json = jsonify(_NO_IMG_WARNING)
    else:
        result_json = jsonify(_NO_IMG_WARNING)
    return result_json


if __name__ == "__main__":
    # Configuration parameters
    flags = init_default_config()
    # Initialize network model and database
    model = init_model(flags.model_architecture, pretrained=flags.pretrained)
    # Set model to evaluation mode
    model.eval()
    preprocessors = init_transforms()
    # Load input mapper dictionary
    vectors_dict = LogosMapper.export_logos_mapper_dictionary()
    # Load faiss database
    index = init_db(flags.index_path)
    # Start service
    serve(app.wsgi_app, port=Options.logo_service_port, threads=True, connection_limit=10000, asyncore_use_poll=True)
