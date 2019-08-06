from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from models.food import Food
from models.food_list import Food_List
from resources.food import Food_Resource

@app.before_first_request
def create_tables():
    db.create_all()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "yeet"
api = Api(app)

app.add_resource(Food_Resource, '/food/<string:name>')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
