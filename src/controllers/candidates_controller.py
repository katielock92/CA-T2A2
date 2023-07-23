from main import db
from models.candidates import Candidate, candidate_schema, candidates_schema
from controllers.auth_controller import authorise_as_admin

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes


candidates = Blueprint("candidates", __name__, url_prefix="/candidates")


# lists all candidates using a GET request, only available to admins:
@candidates.route("/", methods=["GET"])
@jwt_required()
@authorise_as_admin
def get_candidates():
    candidates_list = Candidate.query.order_by(Candidate.id).all()
    result = candidates_schema.dump(candidates_list)
    return jsonify(result)


# allows a logged in user to create a candidate linked to their login ahead of making any applications, using a POST method:
@candidates.route("/", methods=["POST"])
@jwt_required()
def create_candidate():
    user_id = get_jwt_identity()
    query = db.select(Candidate).filter_by(user_id=user_id)
    candidate = db.session.scalar(query)
    if candidate:
        return {"error": "Candidate record already exists for your user id"}, 409
    else:
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
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {"error": "Candidate record already exists for your user id"}, 409


# allows a candidate user to update their own details using a PUT or PATCH request:
@candidates.route("/", methods=["PUT", "PATCH"])
@jwt_required()
def update_candidate():
    user_id = get_jwt_identity()
    body_data = candidate_schema.load(request.get_json(), partial=True)
    query = db.select(Candidate).filter_by(user_id=user_id)
    candidate = db.session.scalar(query)
    if candidate:
        candidate.name = body_data.get("name") or candidate.name
        candidate.phone_number = body_data.get("phone_number") or candidate.phone_number
        db.session.commit()
        return candidate_schema.dump(candidate)
    else:
        return {"error": "You do not have a Candidate record to update"}, 404


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
        return {
            "message": f"The candidate with the id {id} has been deleted successfully"
        }
    else:
        return {"error": f"Candidate not found with id {id}"}, 404
