from main import db
from models.applications import Application, application_schema, applications_schema

from flask import Blueprint, jsonify, request, abort
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity


applications = Blueprint("applications", __name__, url_prefix="/applications")


# lists all applications using a GET request:
# need to add JWT auth to this later
@applications.route("/", methods=["GET"])
def get_all_applications():
    # query = db.select(Application).order_by(Application.application_date.desc())
    # applications = db.session.scalar(query)
    # return applications_schema.dump(applications)

    applications_list = Application.query.all()
    result = applications_schema.dump(applications_list)
    return jsonify(result)


# gets application by id using a GET request:
# need to add JWT auth to this later
@applications.route("/<int:id>", methods=["GET"])
def get_one_application(id):
    query = db.select(Application).filter_by(id=id)
    application = db.session.scalar(query)
    if application:
        return application_schema.dump(application)
    else:
        return {"Error": f"Application not found with id {id}"}, 404


# creates a new application using a POST request:
# need to add JWT auth to this later
@applications.route("/", methods=["POST"])
# @jwt_required()
def create_application():
    body_data = application_schema.load(request.get_json())
    application = Application(
        #job_id = body_data.get("job_id"),
        # candidate_id=get_jwt_identity(),
        application_date=date.today(),
        location=body_data.get("location"),
        working_rights=body_data.get("working_rights"),
        notice_period=body_data.get("notice_period"),
        salary_expectations=body_data.get("salary_expectations"),
    )
    db.session.add(application)
    return application_schema.dump(application), 201

    # application_fields = application_schema.load(request.json)
    # new_application = Application()
    # id set automatically by Flask
    # need to automatically set candidate id once relation is formed
    # new_application.job_id = application_fields["job_id"]
    # new_application.candidate_id = application_fields["candidate_id"] #update this later to use JWT
    # new_application.application_date = date.today()
    # new_application.location = application_fields["location"]
    # new_application.working_rights = application_fields["working_rights"]
    # new_application.notice_period = application_fields["notice_period"]
    # new_application.salary_expectations = application_fields["salary_expectations"]
    # db.session.add(new_application)
    # db.session.commit()
    # return jsonify(application_schema.dump(new_application)), 201


# Katie notes - first application method will work better with nested schemas but it's not automatically doing id and status?