from main import db, ma

from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

VALID_STATUSES = (
    "To review",
    "Recruiter interview",
    "Manager interview",
    "Offer",
    "Rejected",
)


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    application_date = db.Column(db.String) # ensure date format added correctly later
    status = db.Column(db.String(), default="To review")
    candidate_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    location = db.Column(db.String(50))
    working_rights = db.Column(db.String(100))
    notice_period = db.Column(db.String(50))
    salary_expectations = db.Column(
        db.Integer()
    )  # need to find SQL type for money if possible
    # resume
    # cover letter

    # adding parent relationship with Interviews, add cascade later
    interviews = db.relationship("Interview", back_populates="application")

    # adding child relationship with Users and Jobs:
    candidate = db.relationship("User", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")


# create the Application Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class ApplicationSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested(
        "UserSchema", only=["first_name", "last_name", "email", "phone_number"]
    )    
    job = fields.Nested("JobSchema", only=["title"])

    # field validations:
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        # Fields to expose
        fields = (
            "id",
            "job",
            "application_date",
            "candidate",
            "status",
            "location",
            "working_rights",
            "notice_period",
            "salary_expectations"
        )  # add other fields once they are set up


# single application schema, when one applications needs to be retrieved
application_schema = ApplicationSchema()
# multiple application schema, when many applications need to be retrieved
applications_schema = ApplicationSchema(many=True)
