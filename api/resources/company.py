from api.init_database import db


class Company(db.Model):
    __tablename__ = 'companies'
    name = db.Column(db.String, primary_key=True, unique=True)
    current_link = db.Column(db.String)
    previous_link = db.Column(db.String)

    def get_id(self):
        return self.name

    @classmethod
    def json(cls):
        _team_links = cls.query.order_by(cls.name).all()
        return _team_links

    @classmethod
    def export_team_links_to_dict(cls):
        _teams = cls.json()
        _team_links = dict()
        for _teams in _teams:
            _team_links.update({_teams.name: _teams.current_link})
        return _team_links

    @classmethod
    def count(cls):
        return len(cls.query.all())

    @classmethod
    def get_page(cls, page_num, page_limit=10):
        return cls.query.offset(page_num*page_limit - 10).limit(page_limit).all()

def find_team_link_by_name(name):
    return Company.query.get(name)
