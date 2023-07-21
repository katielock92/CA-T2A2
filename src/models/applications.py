from main import db, ma

from marshmallow import fields, validates
from marshmallow.validate import OneOf, Length, And, Regexp, URL


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    application_date = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), default="To review", nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    working_rights = db.Column(db.String(50), nullable=False)
    notice_period = db.Column(db.String(50), nullable=False)
    salary_expectations = db.Column(db.Integer(), nullable=False)
    # using a string rather than a binary datatype for resume for simplicity in this API so that a URL can be used instead:
    resume = db.Column(db.String(), nullable=False)

    # adding parent relationship with Interviews:
    interviews = db.relationship(
        "Interview", back_populates="application") #cascade="all, delete"

    # adding child relationship with Candidates and Jobs:
    candidate = db.relationship("Candidate", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")


# field validations for schemas:
VALID_STATUSES = (
    "To review",
    "Recruiter interview",
    "Manager interview",
    "Offer",
    "Rejected",
)

validate_location = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Location must be at least 2 characters long"),
        Length(max=50, error="Location can only be a maximum of 50 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+",
            error="Location can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)

validate_working_rights = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Working rights must be at least 2 characters long"),
        Length(max=50, error="Working rights can only be a maximum of 50 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+",
            error="Working rights can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)

validate_notice_period = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Notice period must be at least 2 characters long"),
        Length(max=50, error="Notice period can only be a maximum of 50 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+",
            error="Notice period can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)

# create the Application Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class ApplicationSchema(ma.Schema):
    # field validations:
    job_id = fields.Integer(required=True)
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = fields.String(required=True) #validate=URL
    salary_expectations = fields.Integer(required=True)
    

    class Meta:
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

application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)


# additional Schema for displaying applications to authenticated staff:
class ApplicationStaffViewSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested(
        "CandidateSchema", only=["name", "phone_number"]
    )
    job = fields.Nested("JobSchema", only=["title"])


    # field validations:
    job_id = fields.Integer(required=True)
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = fields.String(required=True) #validate=URL
    salary_expectations = fields.Integer(required=True)

    class Meta:
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

application_staff_view_schema = ApplicationStaffViewSchema()
applications_staff_view_schema = ApplicationStaffViewSchema(many=True)


# additional Schema for displaying applications to applicants:
class ApplicationViewSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested(
        "CandidateSchema", only=["name", "phone_number"]
    )
    job = fields.Nested("JobSchema", only=["title"])


    # field validations:
    job_id = fields.Integer(required=True)
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = fields.String(required=True) #validate=URL
    salary_expectations = fields.Integer(required=True)

    class Meta:
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

application_view_schema = ApplicationViewSchema()
applications_view_schema = ApplicationViewSchema(many=True)


# additional Schema for displaying application info on interviews:
class ApplicationInterviewSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested(
        "CandidateSchema", only=["name", "phone_number"]
    )
    job = fields.Nested("JobSchema", only=["title"])

    # field validations:
    job_id = fields.Integer(required=True)
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = fields.String(required=True) #validate=URL
    salary_expectations = fields.Integer(required=True)

    class Meta:
        fields = (
            "job",
            "candidate",
            "location",
            "working_rights",
            "notice_period",
            "salary_expectations",
        )

application_interview_schema = ApplicationInterviewSchema()
applications_interview_schema = ApplicationInterviewSchema(many=True)


# additional Schema for displaying application info on scorecards:
class ApplicationScorecardSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested(
        "CandidateSchema", only=["name"]
    )
    job = fields.Nested("JobSchema", only=["title"])

    # field validations:
    job_id = fields.Integer(required=True)
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = fields.String(required=True) #validate=URL
    salary_expectations = fields.Integer(required=True)

    class Meta:
        fields = (
            "job",
            "candidate"
        )

application_scorecard_schema = ApplicationScorecardSchema()
