import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
ocr_logger = logging.FileHandler('data/logs/ocr.log')
ocr_logger.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s  - %(message)s')
ocr_logger.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(ocr_logger)
