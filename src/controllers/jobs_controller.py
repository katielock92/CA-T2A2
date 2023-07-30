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
from controllers.auth_controller import authorise_as_admin, authorise_as_staff

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")


@jobs.route("/", methods=["GET"])
@jwt_required(optional=True)
def get_open_jobs():
    """Retrieves rows from Jobs table with an "open" status.

    A GET request is used to retrieve all records in the Jobs table that have "Open" in their status field.

    Args:
        None required.

    Input:
        None required.

    Returns:
        Key value pairs for the fields in each record in the Jobs table that meet the filter, in JSON format.
        Depending on the user's authentication, a different schema will be returned resulting in hiring_manager or salary_budget being excluded.
        Records are sorted in ascending order by id.

    Errors:
        No expected errors.
    """
    jobs_list = Job.query.order_by(Job.id).filter_by(status="Open")
    user_id = get_jwt_identity()
    query = db.select(Staff).filter_by(id=user_id)
    user = db.session.scalar(query)
    if user:
        if user.admin:
            result = jobs_admin_schema.dump(jobs_list)
            return jsonify(result)
        else:
            result = jobs_staff_schema.dump(jobs_list)
            return jsonify(result)
    else:
        result = jobs_view_schema.dump(jobs_list)
        return jsonify(result)


@jobs.route("/all/", methods=["GET"])
@jwt_required(optional=True)
def get_all_jobs():
    """Retrieves rows from Jobs table.

    A GET request is used to retrieve all records in the Jobs table.

    Args:
        None required.

    Input:
        None required.

    Returns:
        Key value pairs for the fields in each record in the Jobs table, in JSON format.
        Depending on the user's authentication, a different schema will be returned resulting in hiring_manager or salary_budget being excluded.
        Records are sorted in ascending order by id.

    Errors:
        No expected errors.
    """
    jobs_list = Job.query.order_by(Job.id).all()
    user_id = get_jwt_identity()
    query = db.select(Staff).filter_by(id=user_id)
    user = db.session.scalar(query)
    if user:
        if user.admin:
            result = jobs_admin_schema.dump(jobs_list)
            return jsonify(result)
        else:
            result = jobs_staff_schema.dump(jobs_list)
            return jsonify(result)
    else:
        result = jobs_view_schema.dump(jobs_list)
        return jsonify(result)


@jobs.route("/<int:id>/", methods=["GET"])
@jwt_required(optional=True)
def get_one_job(id):
    """Retrieves a specified row from Jobs table.

    A GET request is used to retrieve the specified record in the Jobs table.

    Args:
        job.id

    Input:
        None required.

    Returns:
        Key value pairs for the fields in the requested record from the Jobs table, in JSON format.
        Depending on the user's authentication, a different schema will be returned resulting in hiring_manager or salary_budget being excluded.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Jobs table.
    """
    query = db.select(Job).filter_by(id=id)
    job = db.session.scalar(query)
    if job:
        user_id = get_jwt_identity()
        stmt = db.select(Staff).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user:
            if user.admin:
                result = jobs_admin_schema.dump(job)
                return jsonify(result)
            else:
                result = jobs_staff_schema.dump(job)
                return jsonify(result)
        else:
            result = jobs_view_schema.dump(job)
            return jsonify(result)
    else:
        return {"Error": f"Job not found with id {id}"}, 404


@jobs.route("/<int:id>/applications/", methods=["GET"])
@jwt_required()
@authorise_as_staff
def get_job_applications(id):
    """Retrieves rows from Applications table for a specified job.id.

    A GET request is used to retrieve all records in the Applications table that contain the specified job.id. Requires a JWT and for a user to have staff permission.

    Args:
        job.id

    Input:
        None required.

    Returns:
        Key value pairs for all fields for each record in the Applications table that meet the job.id filter, in JSON format. Records are sorted in ascending order by application date.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Jobs table.
        403: Displayed if the user does not meet the conditions of the authorise_as_staff wrapper functions.
        401: Displayed if no JWT is provided.
    """
    applications_list = Application.query.order_by(Application.application_date).filter_by(job_id=id)
    if applications_list:
        return applications_staff_view_schema.dump(applications_list)
    else:
        return {"Error": f"Job not found with id {id}"}, 404


@jobs.route("/", methods=["POST"])
@jwt_required()
@authorise_as_staff
def create_job():
    """Creates a new record in the Jobs table, only for staff users.

    A POST request is used to create a new record in the Jobs table. Requires a JWT and for a user to have staff permission.

    Args:
        None required.

    Input:
        title, description, location, department, salary_budget and hiring_manager_id fields, in JSON format.

    Returns:
        Key value pairs for all fields for the new record in the Staff table, in JSON format.

    Errors:
        400: Displayed if a value provided for a field doesn't match a validation criteria.
        409: Displayed if a required field is not provided.
        404: Displayed if the hiring_manager_id provided doesn't match a record in the Staff table.
        403: Displayed if the user does not meet the conditions of the authorise_as_staff wrapper functions.
        401: Displayed if no JWT is provided.
    """
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
            }, 404


@jobs.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_staff
def update_job(id):
    """Updates a specified record in Jobs table, only for staff users.

    A PUT or PATCH request is used to update the specified record in the Jobs table. Requires a JWT and for a user to have staff permission.

    Args:
        job.id

    Input:
        At least one or more of title, description, location, department, salary_budget and hiring_manager_id fields, in JSON format.

    Returns:
        Key value pairs for all fields for the updated record in the Jobs table, in JSON format.

    Errors:
        400: Displayed if a value provided for a field doesn't match a validation criteria.
        404: Displayed if the id provided as an arg doesn't match a record in the Jobs table.
        404: Displayed if the hiring_manager_id provided doesn't match a record in the Staff table.
        403: Displayed if the user does not meet the conditions of the authorise_as_staff wrapper functions.
        401: Displayed if no JWT is provided.
    """
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


@jobs.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_job(id):
    """Deletes a record in Jobs table.

    A DELETE request is used to delete the specified record in the Jobs table. Requires a JWT and for a user to have the admin permission.

    Args:
        job.id

    Input:
        None required.

    Returns:
        A confirmation message in JSON format that the job record has been deleted.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Job table.
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    query = db.select(Job).filter_by(id=id)
    job = db.session.scalar(query)
    if job:
        db.session.delete(job)
        db.session.commit()
        return {"message": f"The {job.title} job has been deleted successfully"}
    else:
        return {"error": f"Job not found with id {id}"}, 404
