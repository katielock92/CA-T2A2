from main import db
from models.applications import Application, application_schema, application_view_schema, application_staff_view_schema, applications_staff_view_schema
from models.users import User

from flask import Blueprint, jsonify, request
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
import functools


applications = Blueprint("applications", __name__, url_prefix="/applications")


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


# creating wrapper function for authorised Recruiter/Hiring Manager only actions:
def authorise_as_staff(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user.access_level == "Recruiter" or user.access_level == "Hiring Manager":
            return fn(*args, **kwargs)
        else:
            return {"error": "You are not authorised to perform this action"}, 403

    return wrapper



# lists all applications using a GET request, only admins can perform this action:
@applications.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_all_applications():
    applications_list = Application.query.all() # need to update for some kind of sort order?
    result = applications_staff_view_schema.dump(applications_list)
    return jsonify(result)


# gets application by id using a GET request, only authenticated staff can perform this action:
@applications.route("/<int:id>", methods=["GET"])
@jwt_required()
@authorise_as_staff
def get_one_application(id):
    query = db.select(Application).filter_by(id=id)
    application = db.session.scalar(query)
    if application:
        return application_staff_view_schema.dump(application)
    else:
        return {"Error": f"Application not found with id {id}"}, 404

# creates a new application using a POST request:
@applications.route("/", methods=["POST"])
@jwt_required()
def create_application():
        application_fields = application_schema.load(request.json)
        new_application = Application()
        new_application.job_id = application_fields["job_id"]
        new_application.candidate_id = get_jwt_identity()
        new_application.application_date = date.today()
        new_application.location = application_fields["location"]
        new_application.working_rights = application_fields["working_rights"]
        new_application.notice_period = application_fields["notice_period"]
        new_application.salary_expectations = application_fields["salary_expectations"]
        db.session.add(new_application)
        db.session.commit()
        return jsonify(application_view_schema.dump(new_application)), 201

# allows an admin to update an application status using a PUT request:
@applications.route("/<int:id>/", methods=["PUT"])
@jwt_required()
@authorise_as_admin
def update_application(id):
    body_data = application_schema.load(request.get_json(), partial=True)
    stmt = db.select(Application).filter_by(id=id)
    application = db.session.scalar(stmt)
    if application:
        application.status = body_data.get("status") or application.status
        db.session.commit()
        return application_staff_view_schema.dump(application)
    else:
        return {"error": f"Application not found with id {id}"}, 404
    

# deletes an application using DELETE method, only admins can perform this action:
@applications.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_application(id):
    stmt = db.select(Application).filter_by(id=id)
    application = db.session.scalar(stmt)
    if application:
        db.session.delete(application)
        db.session.commit()
        return {"message": f"The application with the id {id} has been deleted successfully"}
    else:
        return {"error": f"Application not found with id {id}"}, 404
