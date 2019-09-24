from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_refresh_token_required
from blacklist import BLACKLIST

from models.food import Food
from models.food_list import Food_List_Model
from resources.food import Food_Resource
from resources.food_list import Food_List_Resource
from resources.user import UserRegister, UserLogin, TokenRefresh, UserLogout

from sqlalchemy import event, DDL
from db import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
app.secret_key = "yeet"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

###########Login, Logout, Register###########

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(
    identity
):  # Remember identity is what we define when creating the access token
    if (
        identity == 1
    ):  # instead of hard-coding, we should read from a file or database to get a list of admins instead
        return {"is_admin": True}
    return {"is_admin": False}


# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return (
        decrypted_token["jti"] in BLACKLIST
    )  # Here we blacklist particular JWTs that have been created in the past.


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(
    error
):  # we have to keep the argument here, since it's passed in by the caller internally
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify(
            {"description": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )
###########Routes###########
api.add_resource(Food_Resource, '/food')
api.add_resource(Food_List_Resource, '/food_list/<string:name>')
api.add_resource(UserLogin, "/login")
api.add_resource(UserRegister, "/register")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

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

##########Server########
if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
