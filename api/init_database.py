import os

from flask_sqlalchemy import SQLAlchemy

from api.backup.team_links import team_mapper_backup
from api import app
from utils.logo.cnn.search.training_flags import init_default_config
from utils.logo.logo_handler import (get_links_dict)

db = SQLAlchemy(app)

database_path = app.config['DATABASE_FILE']


def build_sample_db(_user, _team_links, _logos_mapper, _database=database_path):
    if os.path.exists(_database):
        return None

    db.create_all()

    names = [
        'memorhein', 'vitali', 'niko.inas', 'ladosha2'
    ]
    passwords = [
        '883fbdb5614b9fe2b403fedcc6b47e954169e78373d3dd7f3ba6f0c3',
        '2c2e251d21fedf71ffaa63466a90cc9aa969345ca6ca5583f499dcef',
        '4880b53deaa9f1b629d0580a64f7b61b039cce0f72b8f56bebf5eec6',
        '8524a8cc9de5670bad7e8df7eed084872b0d1713257a79c03b082b43'

    ]
    flags = init_default_config()
    vectors_dict = get_links_dict(flags.dict_path)
    # Initialise Users
    for i in range(len(names)):
        user = _user()
        user.username = names[i]
        user.password = passwords[i]
        db.session.add(user)
    # Initialise links
    for _key, _value in team_mapper_backup.items():
        team_link = _team_links()
        team_link.name = _key
        team_link.current_link = _value[0]
        team_link.previous_link = _value[1]
        db.session.add(team_link)
    # Initialise logos mapper
    for _key, _value in vectors_dict.items():
        logos_instance = _logos_mapper()
        logos_instance.id = _key
        logos_instance.company = _value.split('/')[-1].split('_')[0]
        logos_instance.image_path = _value
        db.session.add(logos_instance)

    db.session.commit()
    return
