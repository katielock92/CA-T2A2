from main import db
from models.scorecards import Scorecard, scorecard_schema, scorecard_view_schema
from models.interviews import Interview
from models.staff import Staff
from controllers.auth_controller import authorise_as_admin, authorise_as_staff

from flask import Blueprint, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

scorecards = Blueprint("scorecards", __name__)


@scorecards.route("/", methods=["GET"])
@jwt_required()
@authorise_as_staff
def get_scorecard(interview_id):
    """Retrieves a single row from Scorecards table.

    A GET request is used to retrieve the specified record in the Scorecard table. Requires a JWT and for a user to be an admin user, or be the interviewer.

    Args:
        interview.id

    Input:
        None required.

    Returns:
        Key value pairs for all fields in the requested record in the Scorecard table, in JSON format.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Interviews table, or there is no record in the Scorecards table with a matching interview_id.
        403: Displayed if the user does not meet the conditions of the authorise_as_staff wrapper functions and/or is not either an admin user, or the specified interviewer.
        401: Displayed if no JWT is provided.
    """
    query = db.select(Interview).filter_by(id=interview_id)
    interview = db.session.scalar(query)
    if interview:
        user_id = get_jwt_identity()
        staff_query = db.select(Staff).filter_by(user_id=user_id)
        staff = db.session.scalar(staff_query)
        if interview.interviewer_id == staff.id or staff.admin == True:
            query = db.select(Scorecard).filter_by(interview_id=interview_id)
            scorecard = db.session.scalar(query)
            if scorecard:
                return scorecard_view_schema.dump(scorecard)
            else:
                return {"error": f"Scorecard not found for interview {interview_id}"}, 404
        else:
            return {"error": "You must be an admin or the interviewer to view an interview scorecard"}, 403
    else:
        return {"error": f"Interview not found with id {interview_id}"}, 404


@scorecards.route("/", methods=["POST"])
@jwt_required()
@authorise_as_staff
def create_scorecard(interview_id):
    """Creates a new record in the Scorecards table, only for the interviewer.

    A POST request is used to create a new record in the Scorecards table.
    Requires a JWT, for a user to have staff permission and for the interviewer_id on the interview to be linked to the Staff record of the authenticated user.

    Args:
        interview.id

    Input:
        notes and rating fields, in JSON format.

    Returns:
        Key value pairs for all fields for the new record in the Scorecards table, in JSON format.

    Errors:
        400: Displayed if a value provided for a field doesn't match a validation criteria.
        409: Displayed if a required field is not provided.
        404: Displayed if the interview_id provided doesn't match a record in the Interviews table.
        409: Displayed if there is already a record in the Scorecards record linked to the interview.id provided.
        403: Displayed if the user does not meet the conditions of the authorise_as_staff wrapper functions.
        403: Displayed if the authenticated staff user does not link to the interviewer_id on the specified interview.id.
        401: Displayed if no JWT is provided.
    """
    try:
        query = db.select(Interview).filter_by(id=interview_id)
        interview = db.session.scalar(query)
        if interview:
            user_id = get_jwt_identity()
            staff_query = db.select(Staff).filter_by(user_id=user_id)
            staff_id = db.session.scalar(staff_query)
            if interview.interviewer_id == staff_id.id:
                scorecard_fields = scorecard_schema.load(request.json)
                new_scorecard = Scorecard(
                    interview_id=interview.id,
                    scorecard_datetime=datetime.now(),
                    notes=scorecard_fields["notes"],
                    rating=scorecard_fields["rating"],
                )
                db.session.add(new_scorecard)
                db.session.commit()
                return scorecard_view_schema.dump(new_scorecard), 201
            else:
                return {"error": "Only the interviewer can create a scorecard"}, 403
        else:
            return {"error": f"Interview not found with id {interview_id}"}, 404
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {
                "error": f"Scorecard already exists for interview {interview_id}, please use update to make changes"
            }, 409


@scorecards.route("/", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_staff
def update_scorecard(interview_id):
    """Updates a specified record in the Scorecards table, only for the interviewer.

    A PUT or PATCH request is used to update the specified record in the Scorecards table.
    Requires a JWT, for a user to have staff permission and for the interviewer_id on the interview to be linked to the Staff record of the authenticated user.

    Args:
        interview.id

    Input:
        At least one of notes or rating fields, in JSON format.

    Returns:
        Key value pairs for all fields for the updated record in the Scorecards table, in JSON format.

    Errors:
        400: Displayed if a value provided for a field doesn't match a validation criteria.
        404: Displayed if the interview_id provided doesn't match a record in the Interviews table.
        404: Displayed if there is no matching Scorecards record linked to the interview.id provided.
        403: Displayed if the user does not meet the conditions of the authorise_as_staff wrapper functions.
        403: Displayed if the authenticated staff user does not link to the interviewer_id on the specified interview.id.
        401: Displayed if no JWT is provided.
    """
    query = db.select(Interview).filter_by(id=interview_id)
    interview = db.session.scalar(query)
    if interview:
        user_id = get_jwt_identity()
        staff_query = db.select(Staff).filter_by(user_id=user_id)
        staff_id = db.session.scalar(staff_query)
        if interview.interviewer_id == staff_id.id:
            body_data = scorecard_schema.load(request.get_json(), partial=True)
            query = db.select(Scorecard).filter_by(interview_id=interview_id)
            scorecard = db.session.scalar(query)
            if scorecard:
                scorecard.notes = body_data.get("notes") or scorecard.notes
                scorecard.rating = body_data.get("rating") or scorecard.rating
                db.session.commit()
                return scorecard_view_schema.dump(scorecard)
            else:
                return {"error": f"No scorecard found for interview {interview_id}"}
        else:
            return {"error": "Only the interviewer can edit a scorecard"}, 403
    else:
        return {"error": f"Scorecard not found with for interview {interview_id}"}, 404


@scorecards.route("/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_scorecard(interview_id):
    """Deletes a record in Scorecards table.

    A DELETE request is used to delete the specified record in the Scorecards table. Requires a JWT and for a user to have the admin permission.

    Args:
        interview.id

    Input:
        None required.

    Returns:
        A confirmation message in JSON format that the scorecard record has been deleted.

    Errors:
        404: Displayed if the id provided as an arg doesn't match a record in the Interviews table, and/or there is no matching Scorecard record linked to this interview.id.
        403: Displayed if the user does not meet the conditions of the authorise_as_admin wrapper functions.
        401: Displayed if no JWT is provided.
    """
    query = db.select(Scorecard).filter_by(interview_id=interview_id)
    scorecard = db.session.scalar(query)
    if scorecard:
        db.session.delete(scorecard)
        db.session.commit()
        return {
            "message": f"The scorecard for interview {interview_id} has been deleted successfully"
        }
    else:
        return {"error": f"Interview not found with id {interview_id}"}, 404
