from flask import request, jsonify
from flask_restful import Resource
from cerberus import Validator
from models.food import Food
from db import db

class Food_Resource(Resource):

    @classmethod
    def post(cls):

        ##################REFACTOR##############

        data = {
          'type' : request.args.get('type'),
          'sr' : request.args.get('sr'),
          'ndbno' : int(request.args.get('ndbno')),
          'name' : request.args.get('name'),
          'sd' : request.args.get('sd'),
          'fg' : request.args.get('fg'),
          'ds' : request.args.get('ds'),
          'food_list_id' : int(request.args.get('food_list_id'))
        }

        schema = {
          'type' : { 'type': 'string' },
          'sr' : { 'type' : 'string' },
          'quantity' : { 'type' : 'integer' },
          'ndbno' : { 'required': True, 'type' : 'integer' },
          'name' : { 'required': True, 'type' : 'string' },
          'sd' : {'required': True, 'type' : 'string' },
          'fg' : {'required': True, 'type' : 'string' },
          'ds' : {'required': True, 'type' : 'string' },
          'food_list_id' : { 'required' : True, 'type' : 'integer' }
        }

        v = Validator(schema)
        if not v(data):
            return 'Something wrong with your Validators: {}'.format(v.errors), 400

        try:
            food = Food(**data).save_to_db()
            return 'Food has been saved'
        except Exception as e:
            return 'Food could not be saved, {}'.format(e)
