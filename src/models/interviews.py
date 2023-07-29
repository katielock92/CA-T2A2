from main import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf


class Interview(db.Model):

    """Creates the Interview model in our database.

    Database columns:
        id: A required integer that is automatically serialised, a unique identifier for each interview.
        application_id: A required integer, a foreign key that links to the Applications table.
        candidate_id: A required integer, a foreign key that links to the Candidates table.
        interviewer_id: A required integer, a foreign key that links to the Staff table.
        interview_datetime: A required datetime field, this is the date and time that this interview will be occurring.
        length_mins: A required integer field, this is the expected length of the interview in minutes.
        format: A required string, this is the format/method of the interview.

    Database relationships:
        scorecards: A child of Interviews, the interview.id is a foreign key in the Scorecards table.
        candidates: A parent of Interviews, the candidate.id is a foreign key in the Interviews table.
        staff: A parent of Interviews, the staff.id is a foreign key in the Interviews table.
        applications: A parent of Interviews, the application.id is a foreign key in the Interviews table.
    """

    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    interviewer_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)
    interview_datetime = db.Column(db.DateTime, nullable=False)
    length_mins = db.Column(db.Integer, nullable=False)
    format = db.Column(db.String(), nullable=False)

    scorecards = db.relationship(
        "Scorecard", back_populates="interview", cascade="all, delete"
    )
    application = db.relationship("Application", back_populates="interviews")
    candidate = db.relationship("Candidate", back_populates="interviews")
    interviewer = db.relationship("Staff", back_populates="interviews")


"""Field validations for the schemas.

Defined as variables outside of an individual schema as they are reused across multiple schemas.

"""

VALID_FORMATS = ("Phone", "Video call", "In person")

validate_format = fields.String(
    required=True,
    validate=OneOf(VALID_FORMATS),
    error="Format must be either 'Phone', 'Video call' or 'In person' - please try again",
)
validate_datetime = fields.DateTime(
    required=True,
    format="%Y-%m-%d %H:%M%p",
    error="Please enter date and time in ISO format: YYYY-MM-DD HH:DDAM",
)


class InterviewSchema(ma.Schema):

    """The primary Schema for the Interviews model.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used to load and update values in the Interviews table, but is not returned to users.

    Field validations:
        format: Only accepts input that matches a specified list of values.
        application_id: A required field, integer format.
        interviewer_id: A required field, integer format.
        length_mins: A required field, integer format.
        interview_datetime: Uses the ISO datetime format of YYYY-MM-DD HH:DDAM.

    Class meta: Includes all fields from the model.

    Schema variables:
        interview_schema: When a single Interview record is accessed.
        interviews_schema: When multiple Interview records are accessed.

    """

    format = validate_format
    application_id = fields.Integer(required=True)
    interviewer_id = fields.Integer(required=True)
    length_mins = fields.Integer(required=True)
    interview_datetime = validate_datetime

    class Meta:
        fields = (
            "id",
            "application_id",
            "candidate_id",
            "interviewer_id",
            "interview_datetime",
            "length_mins",
            "format",
        )


interview_schema = InterviewSchema()
interviews_schema = InterviewSchema(many=True)


class InterviewStaffViewSchema(ma.Schema):

    """Additional Schema for the Interviews model for Staff users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data from the Interviews model to authenticated Staff users.

    Nested schemas:
        interviewer is a nested schema from the StaffSchema, which displays the name and title fields of the Staff record linked via the interviewer_id foreign key field.
        application is a nested schema from the ApplicationInterviewSchema, which displays key information about the candidate and their application, linked via the application_id foreign key field.

    Field validations: Same as InterviewSchema.

    Class meta: Includes the following fields:
        id
        application (nested schema)
        interviewer (nested schema)
        interview_datetime
        length_mins
        format

    Schema variables:
        interview_staff_view_schema: When a single Interview record is accessed.
        interviews_staff_view_schema: When multiple Interview records are accessed.

    """

    interviewer = fields.Nested("StaffSchema", only=["name", "title"])
    application = fields.Nested("ApplicationInterviewSchema")

    format = validate_format
    application_id = fields.Integer(required=True)
    interviewer_id = fields.Integer(required=True)
    length_mins = fields.Integer(required=True)
    interview_datetime = validate_datetime

    class Meta:
        fields = (
            "id",
            "application",
            "interviewer",
            "interview_datetime",
            "length_mins",
            "format",
        )


interview_staff_view_schema = InterviewStaffViewSchema()
interviews_staff_view_schema = InterviewStaffViewSchema(many=True)


class InterviewViewSchema(ma.Schema):

    """Additional Schema for the Interviews model for other authenticated users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data from the Applications model to authenticated non-Staff users.

    Nested schemas:
        interviewer is a nested schema from the StaffSchema, which displays the name and title fields of the Staff record linked via the interviewer_id foreign key field.

    Field validations: Same as InterviewSchema.

    Class meta: Includes the following fields:
        id
        interviewer (nested schema)
        interview_datetime
        length_mins
        format

    Schema variables:
        interview_view_schema: When a single Interview record is accessed.
        interviews_view_schema: When multiple Interview records are accessed.

    """

    interviewer = fields.Nested("StaffSchema", only=["name", "title"])

    format = validate_format
    application_id = fields.Integer(required=True)
    interviewer_id = fields.Integer(required=True)
    length_mins = fields.Integer(required=True)
    interview_datetime = validate_datetime

    class Meta:
        fields = (
            "id",
            "interviewer",
            "interview_datetime",
            "length_mins",
            "format",
        )


interview_view_schema = InterviewViewSchema()
interviews_view_schema = InterviewViewSchema(many=True)


class InterviewScorecardSchema(ma.Schema):

    """Additional Schema for the Interviews model for nesting into Scorecard schemas for Staff users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data about the Interview that is linked to a Scorecard record.

    Nested schemas:
        candidate is a nested schema from the CandidateSchema, which displays the name field the Candidate record linked via the candidate_id foreign key field.
        interviewer is a nested schema from the StaffSchema, which displays the name and title fields of the Staff record linked via the interviewer_id foreign key field.

    Field validations: Same as ApplicationSchema.

    Class meta: Only includes the following fields:
        candidate (nested schema)
        interviewer (nested schema)

    Schema variables:
        interview_scorecard_schema: When a single Interview record is accessed.

    """

    candidate = fields.Nested("CandidateSchema", only=["name"])
    interviewer = fields.Nested("StaffSchema", only=["name", "title"])

    class Meta:
        fields = ("candidate", "interviewer")


interview_scorecard_schema = InterviewScorecardSchema()
