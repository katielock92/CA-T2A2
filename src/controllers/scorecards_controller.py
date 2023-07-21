from main import db
from models.scorecards import Scorecard, scorecard_schema, scorecard_view_schema, scorecards_view_schema
from models.staff import Staff

from flask import Blueprint, jsonify, request
from datetime import date, datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
import functools
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes


scorecards = Blueprint("scorecards", __name__, url_prefix="/scorecards")


# creating wrapper function for admin authorised actions:
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            query = db.select(Staff).filter_by(user_id=user_id)
            user = db.session.scalar(query)
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


# lists all scorecards using a GET request, only admins can perform this action:
@scorecards.route("/all", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_all_scorecards():
    scorecards_list = Scorecard.query.all()
    # need to update for some kind of sort order?
    result = scorecards_view_schema.dump(scorecards_list)
    return jsonify(result)



# allows an authorised user to create a new scorecard using a POST request:
@scorecards.route("/", methods=["POST"])
@jwt_required()
@authorise_as_staff
def create_scorecard():
    try:
        scorecard_fields = scorecard_schema.load(request.json)
        new_scorecard = Scorecard()
        new_scorecard.scorecard_datetime = datetime.now()
        new_scorecard.interview_id = scorecard_fields["interview_id"]
        #somehow link to application id by the interview id?
        new_scorecard.notes = scorecard_fields["notes"]
        new_scorecard.rating = scorecard_fields["rating"]
        db.session.add(new_scorecard)
        db.session.commit()
        return jsonify(scorecard_view_schema.dump(new_scorecard)), 201   
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        else:
            return {
                "error": "Invalid application id or interview id provided, please try again."
            }, 409


# allows an admin to update an scorecard notes or rating using a PUT request:
@scorecards.route("/<int:id>/", methods=["PUT"])
@jwt_required()
@authorise_as_admin
def update_scorecard(id):
    body_data = scorecards.load(request.get_json(), partial=True)
    query = db.select(Scorecard).filter_by(id=id)
    scorecard = db.session.scalar(query)
    if scorecard:
        scorecard.notes = body_data.get("notes") or scorecard.notes
        scorecard.rating = body_data.get("rating") or scorecard.rating
        db.session.commit()
        return scorecard_view_schema.dump(scorecard)
    else:
        return {"error": f"Scorecard not found with id {id}"}, 404
    

# deletes a scorecard using DELETE method, only admins can perform this action:
@scorecards.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_scorecard(id):
    query = db.select(Scorecard).filter_by(id=id)
    scorecard = db.session.scalar(query)
    if scorecard:
        db.session.delete(scorecard)
        db.session.commit()
        return {"message": f"The scorecard with the id {id} has been deleted successfully"}
    else:
        return {"error": f"Scorecard not found with id {id}"}, 404