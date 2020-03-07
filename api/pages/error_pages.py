from flask import Blueprint
from flask import render_template

_UNLABELED_LOGOS = 'data/logo/unlabeled'

errors_page = Blueprint('error_page', __name__,
                        template_folder='../../front/templates')


@errors_page.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@errors_page.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500
