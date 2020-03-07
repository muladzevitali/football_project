from flask import Blueprint
from flask import send_from_directory

favicon_page = Blueprint('favicon', __name__,
                         template_folder='../../front/templates',
                         static_folder='../../front/static')


@favicon_page.route('/favicon.ico')
def favicon():
    return send_from_directory(favicon_page.static_folder,
                               'images/favicon.ico', mimetype='image/vnd.microsoft.icon')
