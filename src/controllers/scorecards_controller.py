from main import db
from models.scorecards import (
    Scorecard,
    scorecard_schema,
    scorecard_view_schema
)
from models.interviews import Interview
from models.staff import Staff
from controllers.auth_controller import authorise_as_admin, authorise_as_staff

from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

scorecards = Blueprint("scorecards", __name__)

# displays the scorecard for an interview using a GET request:
@scorecards.route("/", methods=["GET"])
@jwt_required()
@authorise_as_staff
def get_scorecard(interview_id):
    # optional: need to add validation that user is hiring manager for role if not the interviewer?
    query = db.select(Scorecard).filter_by(interview_id=interview_id)
    scorecard = db.session.scalar(query)
    if scorecard:
        return scorecard_view_schema.dump(scorecard)
    else:
        return {"error": f"Scorecard not found for interview {interview_id}"}, 404


# allows an interviewer to create a new scorecard using a POST request:
@scorecards.route("/", methods=["POST"])
@jwt_required()
@authorise_as_staff
def create_scorecard(interview_id):
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
            return scorecard_schema.dump(new_scorecard), 201
        else:
            return {"error": "Only the interviewer can create a scorecard"}, 403
    else:
        return {"error": f"Interview not found with id {interview_id}"}, 404


# allows an admin to update an scorecard notes or rating using a PUT or PATCH request:
@scorecards.route("/", methods=["PUT", "PATCH"])
@jwt_required()
@authorise_as_staff
def update_scorecard(interview_id):
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


# deletes a scorecard using DELETE method, only admins can perform this action:
@scorecards.route("/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_scorecard(interview_id):
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
