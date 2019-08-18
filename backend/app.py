from flask import Flask
from db import db
from flask_restful import Api
from flask_jwt_extended import JWTManager

from models.food import Food
from models.food_list import Food_List_Model
from resources.food import Food_Resource
from resources.food_list import Food_List_Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "yeet"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Food_Resource, '/food')
api.add_resource(Food_List_Resource, '/food_list/<string:name>')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
