from main import db
from models.staff import Staff, staff_schema, staffs_schema
from controllers.auth_controller import authorise_as_admin

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


staff = Blueprint("staff", __name__, url_prefix="/staff")

@staff.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_staff():
    """Retrieves rows from Staff table.

    A GET request is used to retrieve all records in the Staff table. Requires a JWT and for a user to have the admin permission.

    Args:
        None required.

    Input:
        None required.

    Returns:
        Key value pairs for the fields in each record in the Staff table, in JSON format. Records are sorted in ascending order by id.

    Errors:
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    staff_list = Staff.query.order_by(Staff.id).all()
    result = staffs_schema.dump(staff_list)
    return jsonify(result)


# allows an admin user to create staff access linked to a registered user using a POST request:
@staff.route("/", methods=["POST"])
@jwt_required()
@authorise_as_admin
def create_staff():
    """Creates a new record in the Staff table, only for admin users.

    A POST request is used to create a new record in the Staff table, linked to the user.id provided. Requires a JWT and for a user to have the admin permission.

    Args:
        None required.

    Input:
        user.id, name, title and admin fields, in JSON format.

    Returns:
        Key value pairs for all fields for the new record in the Staff table, in JSON format.

    Errors:
        400: Displayed if a value provided for a field doesn't match a validation criteria.
        409: Displayed if a required field is not provided.
        409: Displayed if a Staff record already exists with the user.id provided.
        404: Displayed if the user.id provided doesn't match a record in the Users table.
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    try:
        staff_fields = staff_schema.load(request.json)
        new_staff = Staff()
        new_staff.name = staff_fields["name"]
        new_staff.user_id = staff_fields["user_id"]
        new_staff.title = staff_fields["title"]
        new_staff.admin = staff_fields["admin"]
        db.session.add(new_staff)
        db.session.commit()
        return jsonify(staff_schema.dump(new_staff)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Staff record already exists for this user id"}, 409
        else:
            return {"error": "Invalid user id provided, please try again."}, 404


@staff.route("/", methods=["PUT", "PATCH"])
@jwt_required()
def update_staff():
    """Updates record in Staff table for linked user's own record.

    A PUT or PATCH request is used to update the name or title fields for an authenticated user's record in the Staff table. Requires a JWT.

    Args:
        None required.

    Input:
        At least one of "name" or "title", in JSON format.

    Returns:
        Key value pairs for all fields for the updated record in the Staff table, in JSON format.

    Errors:
        400: Displayed if name or title don't meet validation conditions.
        401: Displayed if no JWT is provided.
        404: Displayed if a JWT is provided, but the user's id does not match a record in the Staff table.
    """
    user_id = get_jwt_identity()
    body_data = staff_schema.load(request.get_json(), partial=True)
    query = db.select(Staff).filter_by(user_id=user_id)
    staff = db.session.scalar(query)
    if staff:
        staff.name = body_data.get("name") or staff.name
        staff.title = body_data.get("title") or staff.title
        db.session.commit()
        return staff_schema.dump(staff)
    else:
        return {"error": "You do not have a Staff record to update"}, 404


@staff.route("/<int:id>/", methods=["PUT"])
@jwt_required()
@authorise_as_admin
def update_staff_admin(id):
    """Updates a specified record in Staff table, only for admin users.

    A PUT or PATCH request is used to update the admin field for a specified record in the Staff table. Requires a JWT and for a user to have the admin permission.

    Args:
        staff.id

    Input:
        Boolean value for "admin".

    Returns:
        Key value pairs for all fields for the updated record in the Staff table, in JSON format.

    Errors:
        400: Displayed if an invalid boolean value is provided.
        404: Displayed if the id provided as an arg doesn't match a record in the Staff table.
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    body_data = staff_schema.load(request.get_json(), partial=True)
    query = db.select(Staff).filter_by(id=id)
    staff = db.session.scalar(query)
    if staff:
        staff.admin = body_data.get("admin") or staff.admin
        staff.name = body_data.get("name") or staff.name
        staff.title = body_data.get("title") or staff.title
        db.session.commit()
        return staff_schema.dump(staff)
    else:
        return {"error": f"Staff not found with id {id}"}, 404


@staff.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_staff(id):
    """Deletes a record in Staff table.

    A DELETE request is used to delete the specified record in the Staff table. Requires a JWT and for a user to have the admin permission.

    Args:
        user.id

    Input:
        None required.

    Returns:
        A confirmation message in JSON format that the staff record has been deleted.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Staff table.
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    query = db.select(Staff).filter_by(id=id)
    staff = db.session.scalar(query)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        return {
            "message": f"The staff record for id: {id} has been deleted successfully"
        }
    else:
        return {"error": f"Staff not found with id {id}"}, 404
