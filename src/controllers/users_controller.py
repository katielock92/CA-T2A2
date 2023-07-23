from main import db, bcrypt
from models.users import User, user_schema, user_view_schema, users_view_schema
from controllers.auth_controller import authorise_as_admin

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


users = Blueprint("users", __name__, url_prefix="/users")


# lists all users using a GET request, only available to admins:
@users.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_users():
    users_list = User.query.order_by(User.id).all()
    result = users_view_schema.dump(users_list)
    return jsonify(result)


# no add functionality within this controller as users are added via the auth controller instead

# allows a user to update their own login email or password using a PUT or PATCH method:
@users.route("/", methods=["PUT", "PATCH"])
@jwt_required()
def update_users():
    user_id = get_jwt_identity()
    body_data = user_schema.load(request.get_json(), partial=True)
    query = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(query)
    user.email = body_data.get("email") or user.email
    if body_data.get("password"):
        user.password = bcrypt.generate_password_hash(body_data.get("password")).decode("utf-8")
    db.session.commit()
    return user_view_schema.dump(user)


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
