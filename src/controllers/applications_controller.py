from main import db
from models.applications import (
    Application,
    application_schema,
    application_view_schema,
    application_staff_view_schema,
    applications_staff_view_schema,
)
from models.candidates import Candidate
from controllers.auth_controller import authorise_as_admin, authorise_as_staff


from flask import Blueprint, jsonify, request
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


applications = Blueprint("applications", __name__, url_prefix="/applications")

@applications.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_all_applications():
    """Retrieves rows from Applications table.

    A GET request is used to retrieve all records in the Applications table. Requires a JWT and for a user to have the admin permission.

    Args:
        None required.

    Input:
        None required.

    Returns:
        Key value pairs for all fields for each record in the Applications table, in JSON format. Records are sorted in ascending order by application date.

    Errors:
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    applications_list = (
        Application.query.order_by(Application.application_date).all()
    )
    result = applications_staff_view_schema.dump(applications_list)
    return jsonify(result)


@applications.route("/<int:id>/", methods=["GET"])
@jwt_required()
@authorise_as_staff
def get_one_application(id):
    """Retrieves a single row from Applications table.

    A GET request is used to retrieve the specified record in the Applications table. Requires a JWT and for a user to be a Staff user.

    Args:
        application.id

    Input:
        None required.

    Returns:
        Key value pairs for all fields in the requested record in the Applications table, in JSON format.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Applications table.
        403: Displayed if the user does not meet the conditions of the authorise_as_staff wrapper functions.
        401: Displayed if no JWT is provided.
    """
    query = db.select(Application).filter_by(id=id)
    application = db.session.scalar(query)
    if application:
        return application_staff_view_schema.dump(application)
    else:
        return {"Error": f"Application not found with id {id}"}, 404


@applications.route("/", methods=["POST"])
@jwt_required()
def create_application():
    """Creates a new record in the Applications table.

    A POST request is used to create a new record in the Applications table. Requires a JWT and for the user to be linked to a record in the Candidates table.

    Args:
        None required.

    Input:
        job_id, resume, location, salary_expectations, notice_period and working_rights fields, in JSON format.

    Returns:
        Key value pairs for all fields for the new record in the Applications table, in JSON format.

    Errors:
        400: Displayed if a value provided for a field doesn't match a validation criteria.
        409: Displayed if a required field is not provided.
        404: Displayed if the job_id provided doesn't match a record in the Jobs table.
        401: Displayed if the authenticated user does not have a linked record in the Candidates table.
        401: Displayed if no JWT is provided.
    """
    user_id = get_jwt_identity()
    query = db.select(Candidate).filter_by(user_id=user_id)
    user = db.session.scalar(query)
    try:
        application_fields = application_schema.load(request.json)
        new_application = Application()
        new_application.job_id = application_fields["job_id"]
        new_application.candidate_id = user.id
        new_application.application_date = date.today()
        new_application.location = application_fields["location"]
        new_application.working_rights = application_fields["working_rights"]
        new_application.notice_period = application_fields["notice_period"]
        new_application.salary_expectations = application_fields["salary_expectations"]
        new_application.resume = application_fields["resume"]
        db.session.add(new_application)
        db.session.commit()
        return jsonify(application_view_schema.dump(new_application)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        else:
            return {"error": "Invalid job id provided, please try again."}, 404
    except AttributeError:
        return {
            "error": "Candidate profile must be created to create an application"
        }, 401


@applications.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin
def update_application(id):
    """Updates a specified record in Applications table, only for admin users.

    A PUT or PATCH request is used to update the status field for a specified record in the Applications table. Requires a JWT and for a user to have the admin permission.

    Args:
        application.id

    Input:
        Valid string value for "status".

    Returns:
        Key value pairs for all fields for the updated record in the Applications table, in JSON format.

    Errors:
        400: Displayed if an invalid status value is provided.
        404: Displayed if the id provided as an arg doesn't match a record in the Applications table.
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    body_data = application_schema.load(request.get_json(), partial=True)
    query = db.select(Application).filter_by(id=id)
    application = db.session.scalar(query)
    if application:
        application.status = body_data.get("status") or application.status
        db.session.commit()
        return application_staff_view_schema.dump(application)
    else:
        return {"error": f"Application not found with id {id}"}, 404


@applications.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_application(id):
    """Deletes a record in Applications table.

    A DELETE request is used to delete the specified record in the Applications table. Requires a JWT and for a user to have the admin permission.

    Args:
        application.id

    Input:
        None required.

    Returns:
        A confirmation message in JSON format that the application record has been deleted.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Applications table.
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    query = db.select(Application).filter_by(id=id)
    application = db.session.scalar(query)
    if application:
        db.session.delete(application)
        db.session.commit()
        return {
            "message": f"The application with the id {id} has been deleted successfully"
        }
    else:
        return {"error": f"Application not found with id {id}"}, 404
