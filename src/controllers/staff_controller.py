from main import db
from models.staff import Staff, staff_schema, staffs_schema

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes


staff = Blueprint("staff", __name__, url_prefix="/staff")


# creating wrapper function for admin authorised actions:
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            stmt = db.select(Staff).filter_by(user_id=user_id)
            user = db.session.scalar(stmt)
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
    except ValidationError:
        return {
            "error": "A required field has not been provided, please try again."
        }, 409
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        else:
            return {
                "error": "Invalid hiring manager id provided, please try again."
            }, 409