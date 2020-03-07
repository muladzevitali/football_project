from json import dumps

from flask import Blueprint
from flask import request, render_template


_UNLABELED_LOGOS = 'data/logo/unlabeled'

contact_page = Blueprint('contact', __name__,
                         template_folder='../../front/templates')


@contact_page.route('/contact/', methods=['GET', 'POST'])
def contact():
    alert = False
    if request.method == 'POST':
        data = dict()
        data["name"] = request.form["name"]
        data["email"] = request.form["email"]
        data["phone"] = request.form["phone"]
        data["subject"] = request.form["subject"]
        data["message"] = request.form["message"]
        with open('messages.txt', 'a+', encoding='utf-8') as file:
            file.write(dumps(data) + ",\n")
        alert = True
    return render_template('contact.html', message_sent=alert)
