from flask_restful import Resource, reqparse
from models.food_list import Food_List_Model

class Food_List_Resource(Resource):

    def post(self, name):
         food_list = Food_List_Model.find_food_list_by_name(name)
         if food_list:
             return {"message": "Food List already Exists"}

         food_list = Food_List_Model(name)
         try:
             food_list.save_to_db()
             return 'Food List Saved'
         except:
             return 'Food list could not be saved to DB'
