from db import db

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(60))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def save_to_db(cls):
        db.session.add(cls)
        db.session.add(cls)

    def delete_from_db(self):
        db.session.delete(self)
        de.session.commit()
