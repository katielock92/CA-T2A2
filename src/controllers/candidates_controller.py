from main import db
from models.staff import Staff
from models.candidates import Candidate, candidate_schema, candidates_schema

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
import functools
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


candidates = Blueprint("candidates", __name__, url_prefix="/candidates")


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


# lists all candidates using a GET request, only available to admins:
@candidates.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_candidates():
    candidates_list = Candidate.query.all()
    result = candidates_schema.dump(candidates_list)
    return jsonify(result)


# allows a logged in user to create a candidate linked to their login ahead of making any applications, using a POST method:
@candidates.route("/", methods=["POST"])
@jwt_required()
def create_candidate():
    # need to check if there is already a candidate for this user before continuing
    try:
        candidate_fields = candidate_schema.load(request.json)
        new_candidate = Candidate()
        new_candidate.name = candidate_fields["name"]
        new_candidate.phone_number = candidate_fields["phone_number"]
        new_candidate.user_id = get_jwt_identity()
        db.session.add(new_candidate)
        db.session.commit()
        return jsonify(candidate_schema.dump(new_candidate)), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        

# deletes a candidate using DELETE method, only admins can perform this action:
@candidates.route("/<int:id>/", methods=["DELETE"])
@jwt_required()
@authorise_as_admin
def delete_candidate(id):
    query = db.select(Candidate).filter_by(id=id)
    candidate = db.session.scalar(query)
    if candidate:
        db.session.delete(candidate)
        db.session.commit()
        return {"message": f"The candidate with the id {id} has been deleted successfully"}
    else:
        return {"error": f"Candidate not found with id {id}"}, 404