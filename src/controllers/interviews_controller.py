from main import db
from models.interviews import Interview, interview_schema, interviews_schema, interview_staff_view_schema, interviews_staff_view_schema, interview_view_schema, interviews_view_schema
from models.users import User

from flask import Blueprint, jsonify, request
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
import functools
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes


interviews = Blueprint("interviews", __name__, url_prefix="/interviews")


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



# lists all interviews using a GET request, only admins can perform this action:
@interviews.route("/all", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_all_interviews():
    interviews_list = Interview.query.all()
    # need to update for some kind of sort order?
    result = interviews_staff_view_schema.dump(interviews_list)
    return jsonify(result)


# lists user's interviews using a GET request - still a work in progress
@interviews.route("/", methods=["GET"])
@jwt_required()
def get_my_interviews():
    user_id = get_jwt_identity()
    # checks if the user has a Recruiter or Hiring Manager permission to see if we should check the interviewer_id:
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user.access_level == "Recruiter" or user.access_level == "Hiring Manager":
        interview_list = Interview.query.filter_by(format="Phone")
        result = interview_staff_view_schema.dump(interview_list)
        if len(result) == 0:
            return {"message": f"No interviews found for {user_id}"}
        else:
            return jsonify(result)
        # if the user does not have this permission, returns the more simplified schema:
    else:
        return {"message": "No interviews found yet"}
        #result = jobs_view_schema.dump(jobs_list)
        #return jsonify(result)

# allows an authorised user to create a new interview using a POST request:
@interviews.route("/", methods=["POST"])
@jwt_required()
@authorise_as_staff
def create_interview():
    try:
        interview_fields = interview_schema.load(request.json)
        new_interview = Interview()
        new_interview.application_id = interview_fields["application_id"]
        new_interview.interviewer_id = interview_fields["interviewer_id"]
        new_interview.interview_datetime = interview_fields["interview_datetime"]
        new_interview.length_mins = interview_fields["length_mins"]
        new_interview.format = interview_fields["format"]
        db.session.add(new_interview)
        db.session.commit()
        return jsonify(interview_staff_view_schema.dump(new_interview)), 201
    except ValidationError:
        return {
            "error": "Interview format must be either 'Phone' or 'Video call' - please try again."
        }, 409
    except KeyError:
        return {
            "error": "A required field has not been provided - please try again."
        }, 409        
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        else:
            return {
                "error": "Invalid application id or interviewer id provided, please try again."
            }, 409


# allows an admin to update an interview using a PUT request:
@interviews.route("/<int:id>/", methods=["PUT"])
@jwt_required()
@authorise_as_admin
def update_interview(id):
    body_data = interview_schema.load(request.get_json(), partial=True)
    stmt = db.select(Interview).filter_by(id=id)
    interview = db.session.scalar(stmt)
    if interview:
        interview.interviewer_id = body_data.get("interview_id") or interview.interviewer_id
        interview.interview_datetime = body_data.get("interview_datetime") or interview.interview_datetime
        interview.format = body_data.get("format") or interview.format
        interview.length_mins = body_data.get("length_mins") or interview.length_mins
        db.session.commit()
        return interview_staff_view_schema.dump(interview)
    else:
        return {"error": f"Interview not found with id {id}"}, 404
    

# deletes an application using DELETE method, only admins can perform this action:
@interviews.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_interview(id):
    stmt = db.select(Interview).filter_by(id=id)
    interview = db.session.scalar(stmt)
    if interview:
        db.session.delete(interview)
        db.session.commit()
        return {"message": f"The interview with the id {id} has been deleted successfully"}
    else:
        return {"error": f"Interview not found with id {id}"}, 404