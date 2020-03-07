from api.init_database import db
from flask_login import AnonymousUserMixin

class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True, unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    @staticmethod
    def is_active():
        """True, as all users are active."""
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    @staticmethod
    def is_anonymous():
        """False, as anonymous users aren't supported."""
        return False


def user_loader(username):
    return User.query.get(username)


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.user_name = 'Guest'
        self.authenticated = False
        self._id = -1

    def get_user_id(self):
        return self._id