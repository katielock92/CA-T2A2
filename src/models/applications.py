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
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    application_date = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), default="To review", nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    working_rights = db.Column(db.String(100), nullable=False)
    notice_period = db.Column(db.String(50), nullable=False)
    salary_expectations = db.Column(db.Integer(), nullable=False)
    # using a string rather than a binary datatype for resume for simplicity in this API so that a URL can be used instead:
    resume = db.Column(db.String(), nullable=False)

    # adding parent relationship with Interviews:
    interviews = db.relationship(
        "Interview", back_populates="application", cascade="all, delete"
    )

    # adding child relationship with Users and Jobs:
    candidate = db.relationship("User", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")


# create the Application Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class ApplicationSchema(ma.Schema):
    # field validations:
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        # Fields to expose
        fields = (
            "id",
            "job_id",
            "application_date",
            "candidate_id",
            "status",
            "location",
            "working_rights",
            "notice_period",
            "salary_expectations",
            "resume"
        )


# single application schema, when one applications needs to be retrieved
application_schema = ApplicationSchema()
# multiple application schema, when many applications need to be retrieved
applications_schema = ApplicationSchema(many=True)


# additional Schema for displaying applications to authenticated staff:
class ApplicationStaffViewSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested(
        "UserSchema", only=["first_name", "last_name", "email", "phone_number"]
    )
    job = fields.Nested("JobSchema", only=["title"])

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
            "salary_expectations",
            "resume"
        )


# single application schema, when one applications needs to be retrieved
application_staff_view_schema = ApplicationStaffViewSchema()
# multiple application schema, when many applications need to be retrieved
applications_staff_view_schema = ApplicationStaffViewSchema(many=True)


# additional Schema for displaying applications to applicants:
class ApplicationViewSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested(
        "UserSchema", only=["first_name", "last_name", "email", "phone_number"]
    )
    job = fields.Nested("JobSchema", only=["title"])

    class Meta:
        # Fields to expose
        fields = (
            "job",
            "application_date",
            "candidate",
            "location",
            "working_rights",
            "notice_period",
            "salary_expectations",
            "resume"
        )


# single application schema, when one applications needs to be retrieved
application_view_schema = ApplicationViewSchema()
# multiple application schema, when many applications need to be retrieved
applications_view_schema = ApplicationViewSchema(many=True)


# additional Schema for displaying application info on interviews:
class ApplicationInterviewSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested(
        "UserSchema", only=["first_name", "last_name", "email", "phone_number"]
    )
    job = fields.Nested("JobSchema", only=["title"])

    class Meta:
        # Fields to expose
        fields = (
            "job",
            "candidate",
            "location",
            "working_rights",
            "notice_period",
            "salary_expectations",
        )


# single application schema, when one applications needs to be retrieved
application_view_schema = ApplicationViewSchema()
# multiple application schema, when many applications need to be retrieved
applications_view_schema = ApplicationViewSchema(many=True)
