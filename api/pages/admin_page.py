import os
from hashlib import sha224

from flask import Blueprint
from flask import request, redirect, url_for, render_template, flash, send_file
from flask_login import login_user, logout_user, current_user, login_required, LoginManager

from api import app
from api.forms.companies import CompanyForm
from api.forms.login import LoginForm
from api.forms.team_mapper import TeamsMapper
from api.init_database import build_sample_db
from api.models.logos import insert_logo, insert_logos_multiple
from api.models.team_links import change_links_all, reset_previous, add_company, delete_item
from api.resources.logos import LogosMapper
from api.resources.company import *
from api.resources.user import *
from flask_paginate import Pagination, get_page_parameter

_UNLABELED_LOGOS = 'data/logo/unlabeled/'

admin_page = Blueprint('admin_page', __name__,
                       template_folder='../../front/templates',
                       static_folder='../../front/static')

build_sample_db(_user=User, _team_links=Company, _logos_mapper=LogosMapper)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(user_loader)
login_manager.anonymous_user = Anonymous


@admin_page.route('/dashboard', methods=["GET"])
@login_required
def admin_landing():
    return render_template("dashboard_main.html")


@admin_page.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    """
    Login page
    :return: None
    """
    # User identification code
    login_form = LoginForm(request.form)
    # Error message
    error = None
    if current_user.authenticated:
        return render_template("dashboard_main.html")
    if request.method == 'POST':
        # Check if correct authorization
        _password = str(request.form['password'])
        _hashed_password = sha224(str(_password).encode('utf-8')).hexdigest()
        user = User.query.get(login_form.username.data)
        if user:
            if user.password == _hashed_password:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                # Redirect in admin panel
                return redirect(url_for('admin_page.admin_landing'))
        else:
            error = 'Permission denied for entered Username and Password'
    return render_template('login.html', form=login_form, error=error)


# Route for handling the login page logic
@admin_page.route('/dashboard/logos/one', methods=['GET', 'POST'])
@login_required
def update_logos_one():
    """
    Update links associated to teams or companies
    :return: None
    """

    form = TeamsMapper()
    if not current_user.authenticated:
        return redirect(url_for('admin_page.admin_landing'))
    if request.method == 'POST':
        # If form was validated
        if 'delete' in request.form:
            image_path = os.path.join(_UNLABELED_LOGOS, request.form.get('delete'))
            if os.path.isfile(image_path):
                os.remove(image_path)
        else:
            response = insert_logo(request.form)
            if response:
                # Insert in database
                new_logo = LogosMapper()
                new_logo.company = response['company']
                new_logo.id = response['id']
                new_logo.image_path = response['path']
                new_logo.image_vector = response['vector']
                db.session.add(new_logo)
                db.session.commit()
    os.makedirs(_UNLABELED_LOGOS, exist_ok=True)
    _unlabeled_images = list()

    for folder in os.listdir(_UNLABELED_LOGOS):
        folder_path = os.path.join(_UNLABELED_LOGOS, folder)
        for image in os.listdir(folder_path):
            _unlabeled_images.append(os.path.join(folder, image))

    per_page_parameter = 18

    page = request.args.get(get_page_parameter(), type=int, default=1)
    images = _unlabeled_images[(page - 1) * per_page_parameter: page * per_page_parameter]
    pagination = Pagination(page=page, total=len(_unlabeled_images), per_page_parameter=per_page_parameter,
                            record_name='Logos', css_framework='bootstrap4')

    return render_template('dashboard_list_logos_one.html', form=form, mapper=Company.json(),
                           images=images, images_folder=_UNLABELED_LOGOS, pagination=pagination)


# Route for handling the login page logic
@admin_page.route("/dashboard/logos/multiple", methods=["GET", "POST"])
@login_required
def update_logos_multiple():
    if request.method == "POST":
        if request.form.get("choose_box", None) == 'Choose an Option':
            flash("PLEASE CHOOSE A COMPANY TO LABEL")
        else:
            responses = insert_logos_multiple(request.form)
            if responses:
                # Insert in database
                for response in responses:
                    new_logo = LogosMapper()
                    new_logo.company = response['company']
                    new_logo.id = response['id']
                    new_logo.image_path = response['path']
                    new_logo.image_vector = response['vector']
                    db.session.add(new_logo)
                    db.session.commit()
    _unlabeled_images = list()
    for folder in os.listdir(_UNLABELED_LOGOS):
        folder_path = os.path.join(_UNLABELED_LOGOS, folder)
        for image in os.listdir(folder_path):
            _unlabeled_images.append(os.path.join(folder, image))

    per_page_parameter = 12
    page = request.args.get(get_page_parameter(), type=int, default=1)
    images = _unlabeled_images[(page - 1) * per_page_parameter: page * per_page_parameter]
    pagination = Pagination(page=page, total=len(_unlabeled_images), per_page_parameter=per_page_parameter,
                            record_name='Logos', css_framework='bootstrap4')
    return render_template("dashboard_list_logos_multiple.html", mapper=Company.json(),
                           images=images, images_folder=_UNLABELED_LOGOS, pagination=pagination)


@admin_page.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    """
    Logout page
    # :param user: string -- user identification number
    :return: Login page
    """
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('admin_page.do_admin_login'))


@admin_page.route('/dashboard/companies/add', methods=['GET', 'POST'])
@login_required
def add_companies():
    """
    Update links associated to teams or companies
    :return: None
    """
    form = CompanyForm(request.form)
    print(request.form)
    if request.method == 'POST' and form.validate():
        _ = add_company(request.form)

    return render_template('dashboard_add_companies.html', form=form, companies=Company.json(),
                           is_authenticated=current_user.authenticated)


@admin_page.route('/dashboard/companies/edit', methods=['GET', 'POST'])
@login_required
def edit_companies():
    form = TeamsMapper()

    if 'reset_previous' in request.form:
        company = {'reset_previous': request.form['reset_previous']}
        _ = reset_previous(company)
    elif 'delete' in request.form:
        company = {'name': request.form['delete']}
        _ = delete_item(company)
    elif form.validate():
        _ = change_links_all(request.form)
    page = request.args.get(get_page_parameter(), type=int, default=1)

    companies = Company.get_page(int(page), page_limit=10)
    pagination = Pagination(page=page, total=Company.count(), per_page_parameter=10, search=False,
                            record_name='Company', css_framework='bootstrap4')
    return render_template("dashboard_edit_companies.html", form=form, companies=companies, pagination=pagination)


@admin_page.route('/dashboard/companies/list', methods=['GET', 'POST'])
@login_required
def list_companies():
    """
    Update links associated to teams or companies
    :return: None
    """
    # If user requested Reset to previous link
    page = request.args.get(get_page_parameter(), type=int, default=1)
    companies = Company.get_page(int(page), page_limit=10)
    pagination = Pagination(page=page, total=Company.count(), per_page_parameter=10, search=False,
                            record_name='Company', css_framework='bootstrap4')
    return render_template('dashboard_list_companies.html', companies=companies, pagination=pagination)


@app.route('/uploads/<folder>/<filename>')
@login_required
def download_file(folder, filename):
    file_path = os.path.join(os.getcwd(), _UNLABELED_LOGOS, folder, filename)
    return send_file(file_path)


@login_required
@admin_page.route('/savevidlink/', methods=['POST'])
def save_video_link():
    text = request.form['linktext']
    file = open('youtube_url.txt', 'w')
    file.write(text)
    return redirect(request.headers.get("Referer"))


@app.context_processor
def get_video_link():
    file = open('youtube_url.txt', 'r')
    line = file.readline()
    return dict(vidlink=line)
