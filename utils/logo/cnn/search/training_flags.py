import argparse

from utils.logo.cnn.search.cnn_files import files as _files
from utils.logo.cnn.search.network_models import RESNET_18


def _add_default_config(arg_parser):
    """Adds default configuration parameters to argument parser
        Args:
           arg_parser - argument parser to add parameters
    """
    arg_parser.add_argument('--model_architecture',
                            type=str,
                            default=RESNET_18,
                            help='Model architecture name')
    # Weights initialization parameters
    arg_parser.add_argument('--pretrained',
                            dest='pretrained',
                            action='store_true',
                            default=True,
                            help='Load pre-trained weights for appropriated network model architecture')
    # Debugging parameters
    arg_parser.add_argument('--debug_vectors',
                            dest='debug_vectors',
                            action='store_true',
                            help='Debug mode for vector similarities')
    # Database configuration
    arg_parser.add_argument('--index_file',
                            dest='index_path',
                            type=str,
                            default=_files.data_file('features.index'),
                            help='Data file for features database')
    arg_parser.add_argument('--n_results',
                            type=int,
                            default=6,
                            help='Number of extracted result from features database')
    arg_parser.add_argument('--dict_file',
                            dest='dict_path',
                            type=str,
                            default=_files.data_file('mapper.json'),
                            help='Path to links file.')


def init_default_config():
    """Initializes default configuration for features vector search
        Returns:
            flags - configuration parameters
    """
    arg_parser = argparse.ArgumentParser('Image search service')
    _add_default_config(arg_parser)
    flags, _ = arg_parser.parse_known_args()

    return flags


def init_config():
    """Initializes configuration parameters container
        Returns:
            flags - training and evaluation configuration parameters
    """
    # Network architecture
    arg_parser = argparse.ArgumentParser('Image search standalone')
    _add_default_config(arg_parser)
    flags, _ = arg_parser.parse_known_args()

    return flags
