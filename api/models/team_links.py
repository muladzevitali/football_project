from api.resources.company import *
from api.init_database import db
_OK = 'OK'


def change_links_all(new_mapper):
    """
    Change values of the first dictionary according to the second one
    :param new_mapper: dictionary -- with new values
    :return: dictionary -- original one
    """
    for key, value in new_mapper.items():
        if key in ['username', 'password']:
            continue
        if new_mapper.get(key):
            print(key, value)
            key = key.replace(' ', '-')
            _team_link = find_team_link_by_name(key)
            _team_link.previous_link = _team_link.current_link
            _team_link.current_link = value
            db.session.add(_team_link)
            db.session.commit()

    return _OK


def reset_previous(team_dict):
    """
    Change values of the first dictionary according to the second one
    :param team_dict: dictionary -- with new value
    :return: dictionary -- original one
    """
    company = team_dict['reset_previous']
    _team_link = find_team_link_by_name(company)
    _team_link.current_link = _team_link.previous_link
    db.session.add(_team_link)
    db.session.commit()

    return _OK


def delete_item(team_dict):
    """
    Change values of the first dictionary according to the second one
    :param team_dict: dictionary -- with new value
    :return: dictionary -- original one
    """
    company = team_dict['name']
    _team_link = find_team_link_by_name(company)
    db.session.delete(_team_link)
    db.session.commit()

    return _OK


def add_company(_form):
    """
    Add new company
    :param _form:
    :return:
    """
    new_company = Company()
    new_company.name = _form['name'].replace(' ', '-')
    new_company.current_link = _form['link']
    new_company.previous_link = _form['link']

    db.session.add(new_company)
    db.session.commit()

    return _OK