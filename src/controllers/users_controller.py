from flask import Blueprint, jsonify, request
from main import db
from models.users import User, user_schema, users_schema


users = Blueprint('users', __name__, url_prefix="/users")

# lists all users using a GET request:
# add JWT auth to this later
@users.route("/", methods=["GET"])
def get_users():
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)


# allows an admin to update a user's permission using a PUT request:
# add JWT auth to this later
@users.route("/<int:id>/", methods=["PUT"])
def update_user():
    pass

# allows an admin to delete a user using a DELETE request:
# add JWT auth to this later
@users.route("/<int:id>/", methods=["DELETE"])
def delete_user():
    pass