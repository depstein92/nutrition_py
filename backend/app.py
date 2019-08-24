from flask import Flask
from db import db
from flask_restful import Api
from flask_jwt_extended import JWTManager

from models.food import Food
from models.food_list import Food_List_Model
from resources.food import Food_Resource
from resources.food_list import Food_List_Resource

from sqlalchemy import event

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "yeet"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

###########Routes###########
api.add_resource(Food_Resource, '/food')
api.add_resource(Food_List_Resource, '/food_list/<string:name>')

###########Create Sample Data###########
@event.listens_for(Food.__table__, 'after_create')
def insert_food_sample_data(*args, **kwargs):
    db.session.add(Food(
      food_list_id=1,
      type="starch",
      sr="6.7.89",
      ndbno=4567,
      name="Sweet Potato",
      sd="A root vegetable high in Potassium",
      fg="Spud",
      ds="USDA"
    ))
    db.session.add(Food(
      food_list_id=1,
      type="starch",
      sr="6.7.89",
      ndbno=4567,
      name="Morel Mushroom",
      sd="A root vegetable high in Oxygen",
      fg="fungus",
      ds="USDA"
    ))
    db.session.add(Food(
      food_list_id=1,
      type="starch",
      sr="6.7.89",
      ndbno=4567,
      name="Oyster Mushroom",
      sd="A root vegetable high in Oxygen",
      fg="fungus",
      ds="USDA"
    ))
    db.session.commit()

@event.listens_for(Food_List_Model.__table__, 'after_create')
def create_food_list_sample_data(*args, **kwargs):
    db.session.add(Food_List_Model(
       id=1,
       name="my Food List"
    ))

#####Server########
if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
