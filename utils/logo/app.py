from flask import Flask

import logging
from logging.handlers import RotatingFileHandler
from configuration import Options
app = Flask(__name__)

handler = RotatingFileHandler(Options.log_logos_service_file, maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)
