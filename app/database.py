from app.__init__ import db
db = db


class UserList(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')
