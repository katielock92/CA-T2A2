from main import db
from models.staff import Staff, staff_schema, staffs_schema

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


staff = Blueprint("staff", __name__, url_prefix="/staff")


# creating wrapper function for admin authorised actions:
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            query = db.select(Staff).filter_by(user_id=user_id)
            user = db.session.scalar(query)
            if user.admin:
                return fn(*args, **kwargs)
            else:
                return {"error": "Not authorised to perform this action"}, 403
        except AttributeError:
            return {"error": "Not authorised to perform this action"}, 403

    return wrapper



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
        else:
            return {
                "error": "Invalid user id provided, please try again."
            }, 409
        

# allows an admin to update a staff member's admin permission using a PUT request:
@staff.route("/<int:id>/", methods=["PUT"])
@jwt_required()
@authorise_as_admin
def update_staff_admin(id):
    body_data = staff_schema.load(request.get_json(), partial=True)
    query = db.select(Staff).filter_by(id=id)
    staff = db.session.scalar(query)
    if staff:
        staff.admin = body_data.get("admin") or staff.admin
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
        return {"message": f"The staff record for id: {id} has been deleted successfully"}
    else:
        return {"error": f"Staff not found with id {id}"}, 404
