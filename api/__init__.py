from flask import Flask
import os

app = Flask(__name__, template_folder='../front/templates', static_folder='../front/static')
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['DATABASE_FILE'] = os.path.join(os.getcwd(), 'database/cutrack.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['path_to_logo_data'] = 'data/logo/unlabeled/'
