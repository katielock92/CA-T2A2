from main import db, ma

from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

VALID_STATUSES = ("Open", "Closed")


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    department = db.Column(db.String(50))
    location = db.Column(db.String(50))
    status = db.Column(db.String(), default="Open", nullable=False)
    salary_budget = db.Column(db.Integer())  # need to find SQL type for money if possible
    # hiring_manager_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # recruiter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # adding child relationship with Users for Recruiter or HM users, does not cascade delete:
    # hiring_manager = db.relationship("User", backref="jobs")
    # recruiter = db.relationship("User", back_populates="jobs")


# creating a Schema with Marshmallow to allow us to serialise Jobs into JSON:
class JobSchema(ma.Schema):
    # nested schemas:
    # hiring_manager = fields.Nested("UserSchema", only=["first_name", "last_name", "email"])
    # recruiter = fields.Nested("UserSchema", only=["first_name", "last_name", "email"])

    # field validations:
    title = fields.String(
        required=True,
        validate=And(
            Length(min=4, error="Job title must be at least 4 characters long"),
            Regexp(
                "^[a-zA-Z0-9() -]+",
                error="Title must contain only letters, numbers, spaces and certain special characters - please try again.",
            ),
        ),
    )

    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        # Fields to expose
        fields = (
            "id",
            "title",
            "department",
            "location",
            "description",
            "hiring_manager",
            "recruiter",
            "status",
            "salary_budget"
        )
        ordered = True


# single job schema, when one job needs to be retrieved
job_schema = JobSchema()
# multiple job schema, when many jobs need to be retrieved
jobs_schema = JobSchema(many=True)