from main import db
from models.staff import Staff, staff_schema, staffs_schema
from controllers.auth_controller import authorise_as_admin

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


staff = Blueprint("staff", __name__, url_prefix="/staff")


# lists all staff using a GET request, only available to admins:
@staff.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_staff():
    staff_list = Staff.query.all()
    result = staffs_schema.dump(staff_list)
    return jsonify(result)


# allows an admin user to create staff access linked to a registered user using a POST request:
@staff.route("/", methods=["POST"])
@jwt_required()
@authorise_as_admin
def create_staff():
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


# allows a Staff user to update their own profile using a PUT request:
@staff.route("/", methods=["PUT"])
@jwt_required()
def update_staff():
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


# allows an admin to update certain fields on a staff member using a PUT request:
@staff.route("/<int:id>/", methods=["PUT"])
@jwt_required()
@authorise_as_admin
def update_staff_admin(id):
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


# allows an admin to delete a staff member using a DELETE request:
@staff.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_staff(id):
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
