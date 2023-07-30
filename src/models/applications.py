from main import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf, Length, And, Regexp


class Application(db.Model):

    """Creates the Application model in our database.

    Database columns:
        id: A required integer that is automatically serialised, a unique identifier for each application.
        job_id: A required integer, a foreign key that links to the Jobs table.
        application_date: A date field, uses the DateTime module to automatically record the date that the application was created.
        status: A required string, specifies the status of the application within the recruitment process.
        candidate_id: A required integer, a foreign key that links to the Candidates table.
        location: A required string, the location of where this candidate is based.
        working_rights: A required string, specifies what rights this candidate has to work in the job's location.
        notice_period: A required string, specifies the user's notice period in their current job.
        salary_expectations: A required integer, indicates the candidate's salary expectations for this job.
        resume: A required string, contains a URL of the candidate's resume. A string was used rather than a binary datatype for simplicity but that could be used if a file upload/storage was available.

    Database relationships:
        interviews: A child of Applications, the application.id is a foreign key in the Interviews table.
        candidates: A parent of Applications, the candidate.id is a foreign key in the Interviews table.
        jobs: A parent of Applications, the job.id is a foreign key in the Interviews table.
    """

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(), default="To review", nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    working_rights = db.Column(db.String(50), nullable=False)
    notice_period = db.Column(db.String(50), nullable=False)
    salary_expectations = db.Column(db.Integer(), nullable=False)
    resume = db.Column(db.String(), nullable=False)

    interviews = db.relationship(
        "Interview", back_populates="application", cascade="all, delete"
    )
    candidate = db.relationship("Candidate", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")


"""Field validations for the schemas.

Defined as variables outside of an individual schema as they are reused across multiple schemas.

"""

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
            "^[a-zA-Z0-9() -]+$",
            error="Location can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)

validate_working_rights = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Working rights must be at least 2 characters long"),
        Length(
            max=50, error="Working rights can only be a maximum of 50 characters long"
        ),
        Regexp(
            "^[a-zA-Z0-9() -]+$",
            error="Working rights can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)

validate_notice_period = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Notice period must be at least 2 characters long"),
        Length(
            max=50, error="Notice period can only be a maximum of 50 characters long"
        ),
        Regexp(
            "^[a-zA-Z0-9() -]+$",
            error="Notice period can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)


validate_resume = fields.String(
    required=True,
    validate=Regexp(
        "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
        error="Invalid URL provided - http or https is required. Please try again.",
    ),
)


class ApplicationSchema(ma.Schema):

    """The primary Schema for the Applications model.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used to load and update values in the Applications table, but is not returned to users.

    Field validations:
        job_id: A required field, integer format.
        application_date: Uses the ISO date format of YYYY-MM-DD.
        location: A regular expression is used so that only letters, numbers, spaces and certain special characters can be used. The field length has a min of 2 and max of 50 characters.
        working_rights: A regular expression is used so that only letters, numbers, spaces and certain special characters can be used. The field length has a min of 2 and max of 50 characters.
        notice_period: A regular expression is used so that only letters, numbers, spaces and certain special characters can be used. The field length has a min of 2 and max of 50 characters.
        status: Only accepts input that matches a specified list of values.
        resume: A regular expression is used to ensure that a correct URL format is provided.
        salary_expectations: A required field, integer format.

    Class meta: Includes all fields from the model.

    Schema variables:
        application_schema: When a single Application record is accessed.
        applications_schema: When multiple Application records are accessed.

    """

    job_id = fields.Integer(required=True)
    application_date = fields.Date(format="%Y-%m-%d")
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = validate_resume
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
            "resume",
        )


application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)


class ApplicationStaffViewSchema(ma.Schema):

    """Additional Schema for the Applications model for Staff users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data from the Applications model to authenticated Staff users.

    Nested schemas:
        candidate is a nested schema from the CandidateSchema, which displays the name and phone_number fields of the Candidate record linked via the candidate_id foreign key field.
        job is a nested schema from the JobSchema, which displays the title field of the Job record linked via the job_id foreign key field.

    Field validations: Same as ApplicationSchema.

    Class meta: Includes all fields from the model except job_id and candidate_id, as nested schemas are used instead.

    Schema variables:
        application_staff_view_schema: When a single Application record is accessed.
        applications_staff_view_schema: When multiple Application records are accessed.

    """

    candidate = fields.Nested("CandidateSchema", only=["name", "phone_number"])
    job = fields.Nested("JobSchema", only=["title"])

    job_id = fields.Integer(required=True)
    application_date = fields.Date(format="%Y-%m-%d")
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = validate_resume
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
            "resume",
        )


application_staff_view_schema = ApplicationStaffViewSchema()
applications_staff_view_schema = ApplicationStaffViewSchema(many=True)


class ApplicationViewSchema(ma.Schema):

    """Additional Schema for the Applications model for Candidate users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data from the Applications model to a Candidate after they create their application.

    Nested schemas:
        candidate is a nested schema from the CandidateSchema, which displays the name and phone_number fields of the Candidate record linked via the candidate_id foreign key field.
        job is a nested schema from the JobSchema, which displays the title field of the Job record linked via the job_id foreign key field.

    Field validations: Same as ApplicationSchema.

    Class meta: Includes all fields from the model except:
        job_id and candidate_id, as nested schemas are used instead
        id
        status

    Schema variables:
        application_view_schema: When a single Application record is accessed.
        applications_view_schema: When multiple Application records are accessed.

    """

    candidate = fields.Nested("CandidateSchema", only=["name", "phone_number"])
    job = fields.Nested("JobSchema", only=["title"])

    job_id = fields.Integer(required=True)
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = validate_resume
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
            "resume",
        )


application_view_schema = ApplicationViewSchema()
applications_view_schema = ApplicationViewSchema(many=True)


class ApplicationInterviewSchema(ma.Schema):

    """Additional Schema for the Applications model for nesting into Interview schemas for Staff users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data about the Application that is linked to an Interview record.

    Nested schemas:
        candidate is a nested schema from the CandidateSchema, which displays the name and phone_number fields of the Candidate record linked via the candidate_id foreign key field.
        job is a nested schema from the JobSchema, which displays the title field of the Job record linked via the job_id foreign key field.

    Field validations: Same as ApplicationSchema.

    Class meta: Only includes the following fields:
        job (nested schema)
        candidate (nested schema)
        location
        working_rights
        notice_period
        salary_expectations

    Schema variables:
        application_interview_schema: When a single Application record is accessed.

    """

    candidate = fields.Nested("CandidateSchema", only=["name", "phone_number"])
    job = fields.Nested("JobSchema", only=["title"])

    job_id = fields.Integer(required=True)
    application_date = fields.Date(format="%Y-%m-%d")
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = validate_resume
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


class ApplicationScorecardSchema(ma.Schema):

    """Additional Schema for the Applications model for nesting into Scorecard schemas for Staff users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data about the Application that is linked to a Scorecard record.

    Nested schemas:
        candidate is a nested schema from the CandidateSchema, which displays the name field the Candidate record linked via the candidate_id foreign key field.
        job is a nested schema from the JobSchema, which displays the title field of the Job record linked via the job_id foreign key field.

    Field validations: Same as ApplicationSchema.

    Class meta: Only includes the following fields:
        job (nested schema)
        candidate (nested schema)

    Schema variables:
        application_scorecard_schema: When a single Application record is accessed.

    """

    candidate = fields.Nested("CandidateSchema", only=["name"])
    job = fields.Nested("JobSchema", only=["title"])

    job_id = fields.Integer(required=True)
    application_date = fields.Date(format="%Y-%m-%d")
    location = validate_location
    working_rights = validate_working_rights
    notice_period = validate_notice_period
    status = fields.String(validate=OneOf(VALID_STATUSES))
    resume = validate_resume
    salary_expectations = fields.Integer(required=True)

    class Meta:
        fields = ("job", "candidate")


application_scorecard_schema = ApplicationScorecardSchema()
