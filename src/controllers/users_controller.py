from main import db
from models.users import User, users_schema
from controllers.auth_controller import authorise_as_admin

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required


users = Blueprint("users", __name__, url_prefix="/users")


# lists all users using a GET request, only available to admins:
@users.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_users():
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)


# no add functionality within this controller as users are added via the auth controller instead

# need to add an edit functionality for users to update their own details


# allows an admin to delete a user using a DELETE request:
@users.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_user(id):
    query = db.select(User).filter_by(id=id)
    user = db.session.scalar(query)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {
            "message": f"The user record for {user.email} (id: {id}) has been deleted successfully"
        }
    else:
        return {"error": f"User not found with id {id}"}, 404
