from main import db
from models.jobs import Job, job_schema, jobs_schema
from models.users import User

from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
import functools

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")


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


# lists all jobs using a GET request:
@jobs.route("/", methods=["GET"])
def get_all_jobs():
    jobs_list = Job.query.all()
    result = jobs_schema.dump(jobs_list)
    return jsonify(result)


# lists all open jobs using a GET request:
@jobs.route("/open/", methods=["GET"])
def get_open_jobs():
    pass
# optional route for later if I have time

# creates a new job using a POST request:
# need to add JWT auth to this later
@jobs.route("/", methods=["POST"])
def create_job():
    job_fields = job_schema.load(request.json)
    new_job = Job()
    new_job.title = job_fields["title"]
    new_job.description = job_fields["description"]
    new_job.department = job_fields["department"]
    new_job.location = job_fields["location"]
    new_job.salary_budget = job_fields["salary_budget"]
    # new_job.hiring_manager_id = job_fields["hiring_manager_id"]
    # add a validation for the hiring manager ID to give a better error?
    db.session.add(new_job)
    db.session.commit()
    return jsonify(job_schema.dump(new_job))


# allows an authorised staff member to update a job using a PUT or POST request:
@jobs.route("/<int:id>/", methods=["PUT", "POST"])
@jwt_required()
@authorise_as_staff
def update_job(id):
    body_data = job_schema.load(request.get_json(), partial=True)
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job:
        job.title = body_data.get("title") or job.title
        job.description = body_data.get("description") or job.description
        job.department = body_data.get("department") or job.department
        job.location = body_data.get("location") or job.location
        job.salary_budget = body_data.get("salary_budget") or job.salary_budget
        job.status = body_data.get("status") or job.status
        # add line to update hiring manager id once that's working in add
        db.session.commit()
        return job_schema.dump(job)
    else:
        return {"error": f"Job not found with id {id}"}, 404


# deletes a job post using DELETE method, only admins can perform this action:
@jobs.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_job(id):
    stmt = db.select(Job).filter_by(id=id)
    job = db.session.scalar(stmt)
    if job:
        db.session.delete(job)
        db.session.commit()
        return {"message": f"The {job.title} job has been deleted successfully"}
    else:
        return {"error": f"Job not found with id {id}"}, 404
