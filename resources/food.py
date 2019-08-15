from flask_restful import Resource, reqparse
from models.food import Food
from db import db

class Food_Resource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
      'name', type=str, required=True, help='name cannot be empty in Food_Resource'
    )

    parser.add_argument(
      'ds', type=str, required=True, help="database source cannot be empty"
    )

    @classmethod
    def get(cls, name):
        food = Food.find_food_by_name(name)
        if food:
            return food.json()
        else:
            return 'Food item not be found'
