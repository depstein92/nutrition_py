from flask_restful import Resource, reqparse
from models.food import Food
from db import db

class Food_Resource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
      'type', type=str, required=False, help="type is empty"
    )
    #release version
    parser.add_argument(
      'sr', type=str, required=False, help="release version is empty"
    )
    #food number
    parser.add_argument(
      'ndbno', type=int, required=True, help="food number is required"
    )
    #name
    parser.add_argument(
      'name', type=str, required=True, help='name is required'
    )
    #short description
    parser.add_argument(
      'sd', type=str, required=True, help="short description required"
    )
    #food group
    parser.add_argument(
      'fg', type=str, required=True, help="food group is required"
    )
    #database source
    parser.add_argument(
      'ds', type=str, required=True, help="database source is required"
    )

    @classmethod
    def post(cls):
        food = Food_Resource.parser.parse_args()
        return 'This route works'
