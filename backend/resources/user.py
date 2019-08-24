from flask import request, jsonify
from flask_restful import Resource
from cerberus import Validator
from db import db
from models import UserModel

class UserRegister(Resource):
    def post(self):
        data = {
          "username" : request.args.get("username"),
          "password" : request.args.get("password"),
          "id" : request.args.get('id')
        }

        schema = {
          "username" : { "type", "string", "required" : True },
          "password" : { "type", "string", "required" : True },
          "id" : {  "type" : "integer", "required": True }
        }

        v = Validator(schema)
        if not in v(data):
            return { "message" : "Not correct data type, failed in validators"}, 505

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    def post(self):
        data = {
          "username" : request.args.get("username"),
          "password" : request.args.get("password"),
          "id" : request.args.get('id')
        }

        schema = {
          "username" : { "type", "string", "required" : True },
          "password" : { "type", "string", "required" : True },
          "id" : {  "type" : "integer", "required": True }
        }

        v = Validator(schema)
        if not in v(data):
            return { "message" : "Not correct data type, failed in validators"}, 505

        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "User <id={}> successfully logged out.".format(user_id)}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
