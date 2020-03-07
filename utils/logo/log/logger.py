import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
logo_logger = logging.FileHandler('data/logs/logo.log')
logo_logger.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s  - %(message)s')
logo_logger.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(logo_logger)
