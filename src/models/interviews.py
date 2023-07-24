from main import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf


class Interview(db.Model):
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

    # adding parent relationship with Scorecards:
    scorecards = db.relationship(
        "Scorecard", back_populates="interviews", cascade="all, delete"
    )

    # add child relationships with Applications, Candidates and Staff:
    application = db.relationship("Application", back_populates="interviews")
    candidate = db.relationship("Candidate", back_populates="interviews")
    interviewer = db.relationship("Staff", back_populates="interviews")


# field validations for schemas:
VALID_FORMATS = ("Phone", "Video call", "In person")

validate_format = fields.String(
    required=True,
    validate=OneOf(VALID_FORMATS),
    error="Format must be either 'Phone', 'Video call' or 'In person' - please try again",
)
validate_datetime = fields.DateTime(required=True, format="%Y-%m-%d %H:%M%p", error="Please enter date and time in ISO format: YYYY-MM-DD HH:DDAM")


# create the primary Interview Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class InterviewSchema(ma.Schema):
    # field validations:
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


# additional Schema for displaying interviews to authenticated staff:
class InterviewStaffViewSchema(ma.Schema):
    # nested schemas:
    interviewer = fields.Nested("StaffSchema", only=["name", "title"])
    application = fields.Nested("ApplicationInterviewSchema")

    # field validations:
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


# additional Schema for displaying interviews to other authenticated users:

class InterviewViewSchema(ma.Schema):
    # nested schemas:
    interviewer = fields.Nested("StaffSchema", only=["name", "title"])

    # field validations:
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


# additional Schema for displaying select application and interview information on scorecards:


class InterviewScorecardSchema(ma.Schema):
    # nested schemas:
    candidate = fields.Nested("CandidateSchema", only=["name"])
    interviewer = fields.Nested("StaffSchema", only=["name", "title"])

    class Meta:
        fields = ("candidate", "interviewer")


interview_scorecard_schema = InterviewScorecardSchema()
