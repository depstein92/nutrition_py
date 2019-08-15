from flask_restful import Resource, reqparse
from models.food_list import Food_List_Model

class Food_List_Resource(Resource):
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "foods": [food.json() for food in self.food.all()]
        }

    def get(self, name):
        if name == 'all':
            all_food = Food_List_Model.find_all()
            if all_food:
                formated_list = [food.json() for food in all_food]
                return {'all_foods' : '{}'.format(formated_list) }
            else:
                return {'message': 'Food List cannot be found'}
        else:
            food_list = Food_List_Model.find_food_list_by_name(name)
            if food_list:
                return food_list.json()
            else:
                return 'Food List not found'

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
