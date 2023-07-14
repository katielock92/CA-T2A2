from main import db
from models.jobs import Job, job_schema, jobs_schema

from flask import Blueprint, jsonify, request, abort

jobs = Blueprint("jobs", __name__, url_prefix="/jobs")

# lists all jobs using a GET request:
@jobs.route("/", methods=["GET"])
def get_jobs():
    jobs_list = Job.query.all()
    result = jobs_schema.dump(jobs_list)
    return jsonify(result)

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
    new_job.hiring_manager_id = job_fields["hiring_manager_id"]
    # add a validation for the hiring manager ID to give a better error?
    db.session.add(new_job)
    db.session.commit()
    return jsonify(job_schema.dump(new_job))


# Finally, we round out our CRUD resource with a DELETE method
@jobs.route("/<int:id>/", methods=["DELETE"])
def delete_job(id):
    # #get the user id invoking get_jwt_identity
    # user_id = get_jwt_identity()
    # #Find it in the db
    # user = User.query.get(user_id)
    # #Make sure it is in the database
    # if not user:
    #     return abort(401, description="Invalid user")
    # # Stop the request if the user is not an admin
    # if not user.admin:
    #     return abort(401, description="Unauthorised user")
    # find the job
    #job = job.query.filter_by(id=id).first()
    # return an error if the card doesn't exist
    #if not Job:
        #return abort(400, description= "Job doesn't exist")
    # Delete the job from the database and commit
    #db.session.delete(job)
    #db.session.commit()
    # return the job in the response
    #return jsonify(job_schema.dump(job))
    return "Job deleted"