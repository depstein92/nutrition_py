from db import db

class Food(db.Model):
    __tablename__ = "food"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    sr = db.Column(db.String(50)) #release version
    ndbno = db.Column(db.Integer) #nbd food number
    name = db.Column(db.String(80), unique=True)
    sd = db.Column(db.String(120)) #short description
    fg = db.Column(db.String(120)) #food group
    ds = db.Column(db.String(60)) #database source

    food_list_id = db.Column(db.Integer, db.ForeignKey("food_list.id"))
    food_list = db.relationship("Food_List_Model")

    def __init__(self, type, sr, ndbno, name, sd, fg, ds, food_list_id):
        self.type = type
        self.sr = sr
        self.ndbno = ndbno
        self.name = name
        self.sd = sd
        self.fg = fg
        self.ds = ds
        self.food_list_id = food_list_id

    @classmethod
    def find_food_by_name(cls):
        return cls.query.filter_by(name=name).first()

    def json(self):
        return {
            "id": self.id,
            "type": self.type,
            "sr": self.sr,
            "ndbno": self.ndbno,
            "name": self.name,
            "sd": self.sd,
            "fg": self.fg,
            "ds": self.ds,
            "food_list_id": self.food_list_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.sesssoin.delete(self)
        de.session.commit()
