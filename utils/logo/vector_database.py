import os
import faiss
import numpy as np
from faiss import IDSelectorBatch


_OK = 'ok'


def init_db(index_path, dim=512):
    if os.path.isfile(index_path):
        index = faiss.read_index(index_path)
    else:
        index = faiss.index_factory(dim, 'IDMap,Flat')
    return index


def train_db(index):

    index.train()


def insert_vector_and_id(image_id, features_vector, index_faiss):

    id_array = np.array([image_id], dtype=np.int64)
    vector_array = features_vector if isinstance(features_vector, np.ndarray) else np.array(features_vector)
    index_faiss.add_with_ids(vector_array, id_array)

    return _OK


def update_index(image_id, image_vector, index_faiss=None):

    id_array = np.array([image_id], dtype=np.int64)
    idsel = IDSelectorBatch(id_array.shape[0], faiss.swig_ptr(id_array))
    index_faiss.remove_ids(idsel)
    vector_array = np.array([image_vector], dtype=np.float32)
    index_faiss.add_with_ids(vector_array, id_array)


def find_vector(features_vector, n_results=10, index_faiss=None):

    distance, index_res = index_faiss.search(features_vector, n_results)
    result_data = index_res[0][0]
    distance = distance[0][0]

    return result_data, distance
