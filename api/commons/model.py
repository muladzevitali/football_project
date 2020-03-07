from utils.detection.flags import init_detection_config
from utils.detection.yolo.utils.loader import load_model

LABELS = ['TEXT', 'LOGO']
flags = init_detection_config()
label_detector = load_model(flags)
height = label_detector.net_info['height']
