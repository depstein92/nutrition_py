from flask import jsonify
from flask_restful import Resource
from proj.tasks import get_user_data

class Sample_Data(Resource):

    @staticmethod
    def get():
        user_data = get_user_data.apply_async(countdown=20)
        user_data.wait()

        return jsonify({
         'message': 'Success!',
         'data': ''.format(user_data)
        })
