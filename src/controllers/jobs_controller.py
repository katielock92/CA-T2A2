from main import db
from models.jobs import (
    Job,
    job_schema,
    jobs_view_schema,
    job_admin_schema,
    jobs_admin_schema,
    jobs_staff_schema,
)
from models.applications import Application, applications_staff_view_schema
from models.staff import Staff

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import functools
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")


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


# creating wrapper function for staff only actions:
def authorise_as_staff(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            query = db.select(Staff).filter_by(user_id=user_id)
            user = db.session.scalar(query)
            if user:
                return fn(*args, **kwargs)
            else:
                return {"error": "Not authorised to perform this action"}, 403
        except AttributeError:
            return {"error": "Not authorised to perform this action"}, 403

    return wrapper


# lists open jobs using a GET request:
@jobs.route("/", methods=["GET"])
@jwt_required(optional=True)
def get_open_jobs():
    jobs_list = Job.query.filter_by(status="Open")
    # find a way to sort these?
    user_id = get_jwt_identity()
    # checks if a user is a staff member and returns a more detailed schema if they are:
    query = db.select(Staff).filter_by(id=user_id)
    user = db.session.scalar(query)
    if user:
        if user.admin:
            result = jobs_admin_schema.dump(jobs_list)
            return jsonify(result)
        else:
            result = jobs_staff_schema.dump(jobs_list)
            return jsonify(result)
    # if not logged in or not staff, a more simplified schema is returned:
    else:
        result = jobs_view_schema.dump(jobs_list)
        return jsonify(result)


# lists all jobs (regardless of status) using a GET request:
@jobs.route("/all/", methods=["GET"])
@jwt_required(optional=True)
def get_all_jobs():
    # find a way to sort these by id?
    jobs_list = Job.query.all()
    user_id = get_jwt_identity()
    # checks if a user is staff and returns a more detailed schema if they are:
    query = db.select(Staff).filter_by(id=user_id)
    user = db.session.scalar(query)
    if user:
        if user.admin:
            result = jobs_admin_schema.dump(jobs_list)
            return jsonify(result)
        else:
            result = jobs_staff_schema.dump(jobs_list)
            return jsonify(result)
    # if not logged in or not staff, a more simplified schema is returned:
    else:
        result = jobs_view_schema.dump(jobs_list)
        return jsonify(result)


# returns an individual job by id using a GET request, the schema depending on user permission:
@jobs.route("/<int:id>/", methods=["GET"])
@jwt_required(optional=True)
def get_one_job(id):
    query = db.select(Job).filter_by(id=id)
    job = db.session.scalar(query)
    if job:
        user_id = get_jwt_identity()
        # checks if a user is a staff member and returns a more detailed schema if they are:
        stmt = db.select(Staff).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user:
            if user.admin:
                result = jobs_admin_schema.dump(job)
                return jsonify(result)
            else:
                result = jobs_staff_schema.dump(job)
                return jsonify(result)
        # if not logged in or not staff, a more simplified schema is returned:
        else:
            result = jobs_view_schema.dump(job)
            return jsonify(result)
    else:
        return {"Error": f"Job not found with id {id}"}, 404


# returns all applications for a particular job id using a GET request, for authorised users only:
@jobs.route("/<int:id>/applications/", methods=["GET"])
@jwt_required()
@authorise_as_staff
def get_job_applications(id):
    applications_list = Application.query.filter_by(job_id=id)
    # find a way to sort these by date?
    if applications_list:
        return applications_staff_view_schema.dump(applications_list)
    else:
        return {"Error": f"Job not found with id {id}"}, 404


# allows an authorised user to create a new job using a POST request:
@jobs.route("/", methods=["POST"])
@jwt_required()
@authorise_as_staff
def create_job():
    try:
        job_fields = job_schema.load(request.json)
        new_job = Job()
        new_job.title = job_fields["title"]
        new_job.description = job_fields["description"]
        new_job.department = job_fields["department"]
        new_job.location = job_fields["location"]
        new_job.salary_budget = job_fields["salary_budget"]
        new_job.hiring_manager_id = job_fields["hiring_manager_id"]
        db.session.add(new_job)
        db.session.commit()
        return jsonify(job_admin_schema.dump(new_job)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        else:
            return {
                "error": f"Invalid hiring manager id provided, please try again."
            }, 400


# allows an authorised staff member to update a job using a PUT or POST request:
@jobs.route("/<int:id>/", methods=["PUT", "POST"])
@jwt_required()
@authorise_as_staff
def update_job(id):
    body_data = job_schema.load(request.get_json(), partial=True)
    query = db.select(Job).filter_by(id=id)
    job = db.session.scalar(query)
    if job:
        try:
            job.title = body_data.get("title") or job.title
            job.description = body_data.get("description") or job.description
            job.department = body_data.get("department") or job.department
            job.location = body_data.get("location") or job.location
            job.salary_budget = body_data.get("salary_budget") or job.salary_budget
            job.status = body_data.get("status") or job.status
            job.hiring_manager_id = (
                body_data.get("hiring_manager_id") or job.hiring_manager_id
            )
            db.session.commit()
            return job_admin_schema.dump(job)
        except IntegrityError:
            return {
                "error": f"Invalid hiring manager id provided, please try again."
            }, 400
    else:
        return {"error": f"Job not found with id {id}"}, 404


# deletes a job post using DELETE method, only admins can perform this action:
@jobs.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_job(id):
    query = db.select(Job).filter_by(id=id)
    job = db.session.scalar(query)
    if job:
        db.session.delete(job)
        db.session.commit()
        return {"message": f"The {job.title} job has been deleted successfully"}
    else:
        return {"error": f"Job not found with id {id}"}, 404
