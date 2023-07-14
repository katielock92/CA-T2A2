from main import db
from models.applications import Application, application_schema, applications_schema

from flask import Blueprint, jsonify, request, abort
from datetime import date


applications = Blueprint("applications", __name__, url_prefix="/applications")

# lists all applications using a GET request:
# need to add JWT auth to this later
@applications.route("/", methods=["GET"])
def get_applications():
    applications_list = Application.query.all()
    result = applications_schema.dump(applications_list)
    return jsonify(result)

# creates a new application using a POST request:
# need to add JWT auth to this later
@applications.route("/", methods=["POST"])
def create_application():
    application_fields = application_schema.load(request.json)
    new_application = Application()
    # id set automatically by Flask
    # need to automatically set candidate id once relation is formed
    new_application.job_id = application_fields["job_id"]
    new_application.application_date = date.today()
    new_application.location = application_fields["location"]
    new_application.working_rights = application_fields["working_rights"]
    new_application.notice_period = application_fields["notice_period"]
    new_application.salary_expectations = application_fields["salary_expectations"]
    db.session.add(new_application)
    db.session.commit()
    return jsonify(application_schema.dump(new_application))

