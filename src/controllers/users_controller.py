from main import db
from models.users import User, user_schema, users_schema

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools
from marshmallow import ValidationError


users = Blueprint("users", __name__, url_prefix="/users")


# creating wrapper function for admin authorised actions:
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.access_level == "Recruiter":
            return fn(*args, **kwargs)
        else:
            return {
                "error": "You are not authorised to perform this action - please contact a Recruiter"
            }, 403

    return wrapper


# lists all users using a GET request, only available to admins:
@users.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_users():
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return jsonify(result)


# allows an admin to update a user's permission using a PUT request:
@users.route("/<int:id>/", methods=["PUT", "POST"])
@jwt_required()
@authorise_as_admin
def update_user(id):
    try:
        body_data = user_schema.load(request.get_json(), partial=True)
        stmt = db.select(User).filter_by(id=id)
        user = db.session.scalar(stmt)
        if user:
            user.access_level = body_data.get("access_level") or user.access_level
            db.session.commit()
            return user_schema.dump(user)
        else:
            return {"error": f"User not found with id {id}"}, 404
    except ValidationError:
        return {
            "error": "Access level must be one of: Candidate, Hiring Manager or Recruiter."
        }, 409


# allows an admin to delete a user using a DELETE request:
@users.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_user(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.scalar(stmt)
    if user:
        db.session.delete(user)
        db.session.commit()
        return {"message": f"The user record for {user.email} has been deleted successfully"}
    else:
        return {"error": f"User not found with id {id}"}, 404
