from main import db
from models.staff import Staff
from models.candidates import Candidate
from models.interviews import (
    Interview,
    interview_schema,
    interview_staff_view_schema,
    interviews_staff_view_schema,
    interviews_view_schema,
)
from controllers.auth_controller import authorise_as_admin, authorise_as_staff
from controllers.scorecards_controller import scorecards

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


interviews = Blueprint("interviews", __name__, url_prefix="/interviews")
interviews.register_blueprint(scorecards, url_prefix="/<int:interview_id>/scorecards")


# lists all interviews using a GET request, only admins can perform this action:
@interviews.route("/all", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_all_interviews():
    interviews_list = Interview.query.order_by(Interview.interview_datetime).all()
    result = interviews_staff_view_schema.dump(interviews_list)
    return jsonify(result)


# lists user's interviews using a GET request:
@interviews.route("/", methods=["GET"])
@jwt_required()
def get_my_interviews():
    user_id = get_jwt_identity()
    try:
        # checks for user in Staff:
        query = db.select(Staff).filter_by(user_id=user_id)
        user = db.session.scalar(query)
        if user:
            interview_list = Interview.query.order_by(Interview.interview_datetime).filter_by(interviewer_id=user.id)
            result = interviews_staff_view_schema.dump(interview_list)
            if len(result) > 0:
                return jsonify(result)
            else: pass # if they match a Staff record but have no interviews, using pass to use the one return line as for Candidates
        else:
            # now checking Candidates for user:
            query = db.select(Candidate).filter_by(user_id=user_id)
            user = db.session.scalar(query)
            if user:
                interview_list = Interview.query.order_by(Interview.interview_datetime).filter_by(candidate_id=user.id)
                result = interviews_view_schema.dump(interview_list)
                if len(result) > 0:
                    return jsonify(result)
                else: pass
            return {"message": "You have no scheduled interviews."}
    except AttributeError:
        # this will catch any registered users who are not yet in either the Staff or Candidate db:
        return {"message": "You have no scheduled interviews."}


# allows an authorised user to create a new interview using a POST request:
@interviews.route("/", methods=["POST"])
@jwt_required()
@authorise_as_staff
def create_interview():
    try:
        interview_fields = interview_schema.load(request.json)
        new_interview = Interview()
        new_interview.application_id = interview_fields["application_id"]
        new_interview.candidate_id = interview_fields[
            "candidate_id"
        ]  # update this later to pull based on application id?
        new_interview.interviewer_id = interview_fields["interviewer_id"]
        new_interview.interview_datetime = interview_fields["interview_datetime"]
        new_interview.length_mins = interview_fields["length_mins"]
        new_interview.format = interview_fields["format"]
        db.session.add(new_interview)
        db.session.commit()
        return jsonify(interview_staff_view_schema.dump(new_interview)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        else:
            return {
                "error": "Invalid id provided for application, candidate or interviewer, please try again."
            }, 409


# allows an admin to update an interview using a PUT or PATCH request:
@interviews.route("/<int:id>/", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_admin
def update_interview(id):
    body_data = interview_schema.load(request.get_json(), partial=True)
    query = db.select(Interview).filter_by(id=id)
    interview = db.session.scalar(query)
    if interview:
        interview.interviewer_id = (
            body_data.get("interviewer_id") or interview.interviewer_id
        )
        interview.interview_datetime = (
            body_data.get("interview_datetime") or interview.interview_datetime
        )
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
    query = db.select(Interview).filter_by(id=id)
    interview = db.session.scalar(query)
    if interview:
        db.session.delete(interview)
        db.session.commit()
        return {
            "message": f"The interview with the id {id} has been deleted successfully"
        }
    else:
        return {"error": f"Interview not found with id {id}"}, 404
