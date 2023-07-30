from main import db, bcrypt
from models.users import User, user_schema, user_view_schema, users_view_schema
from controllers.auth_controller import authorise_as_admin

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_users():
    """Retrieves rows from Users table.

    A GET request is used to retrieve all records in the Users table. Requires a JWT and for a user to have the admin permission.

    Args:
        None required.

    Input:
        None required.

    Returns:
        Key value pairs for the email and id fields for each record in the Users table, in JSON format. Records are sorted in ascending order by id.

    Errors:
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    users_list = User.query.order_by(User.id).all()
    result = users_view_schema.dump(users_list)
    return jsonify(result)


@users.route("/", methods=["PUT", "PATCH"])
@jwt_required()
def update_users():
    """Updates record in Users table.

    A PUT or PATCH request is used to update the email or password fields for an authenticated user's record in the Users table. Requires a JWT.

    Args:
        None required.

    Input:
        At least one of "email" or "password", in JSON format.

    Returns:
        Key value pairs for the email and id fields for the updated record in the Users table, in JSON format.

    Errors:
        xxx
        401: Displayed if no JWT is provided.
    """
    user_id = get_jwt_identity()
    body_data = user_schema.load(request.get_json(), partial=True)
    query = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(query)
    user.email = body_data.get("email") or user.email
    if body_data.get("password"):
        user.password = bcrypt.generate_password_hash(body_data.get("password")).decode("utf-8")
    db.session.commit()
    return user_view_schema.dump(user)


@users.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_user(id):
    """Deletes a record in Users table.

    A DELETE request is used to delete the specified record in the Users table. Requires a JWT and for a user to have the admin permission.

    Args:
        user.id

    Input:
        None required.

    Returns:
        A confirmation message in JSON format that the user record has been deleted.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Users table.
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """

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
