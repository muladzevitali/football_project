from api.init_database import db


class LogosMapper(db.Model):
    __tablename__ = 'logos'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    company = db.Column(db.String)
    image_path = db.Column(db.String)
    image_vector = db.column(db.ARRAY)

    def get_id(self):
        return self.company

    @classmethod
    def json(cls):
        _team_name = cls.query.order_by(cls.company).all()
        return _team_name

    @classmethod
    def export_logos_mapper_dictionary(cls):
        _logos_rows = cls.json()
        _mapper = dict()
        for logo in _logos_rows:
            _mapper.update({str(logo.id): logo.company})

        return _mapper

    def list_names(self):
        _teams = self.json()


def find_team_link_by_name(company):
    return LogosMapper.query.get(company)


