from main import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf

VALID_FORMATS = ("Phone", "Video call")


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    interviewer_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)
    interview_datetime = db.Column(db.DateTime, nullable=False)
    length_mins = db.Column(db.Integer, nullable=False)
    format = db.Column(db.String(), nullable=False)

    # adding parent relationship with Scorecards:
    scorecards = db.relationship("Scorecard", back_populates="interviews") #cascade="all, delete"

    # add child relationships with Applications, Candidates and Staff:
    application = db.relationship("Application", back_populates="interviews")
    candidate = db.relationship("Candidate", back_populates="interviews")
    interviewer = db.relationship("Staff", back_populates="interviews")
    


# create the Interview Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class InterviewSchema(ma.Schema):
    # field validations:
    format = fields.String(validate=OneOf(VALID_FORMATS), error="Format must be either 'Phone' or 'Video call' - please try again")

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


# single interview schema, when one interview needs to be retrieved
interview_schema = InterviewSchema()
# multiple interviews schema, when many interviews need to be retrieved
interviews_schema = InterviewSchema(many=True)


# additional Schema for displaying interviews to authenticated staff:

class InterviewStaffViewSchema(ma.Schema):
    # nested schemas:
    interviewer = fields.Nested(
        "StaffSchema", only=["name", "title"]
    )
    application = fields.Nested(
        "ApplicationInterviewSchema"
    )
    
    class Meta:
        fields = (
            "id",
            "application",
            "interviewer",
            "interview_datetime",
            "length_mins",
            "format",
        )


# single interview schema, when one interview needs to be retrieved
interview_staff_view_schema = InterviewStaffViewSchema()
# multiple interviews schema, when many interviews need to be retrieved
interviews_staff_view_schema = InterviewStaffViewSchema(many=True)


# additional Schema for displaying interviews to other authenticated useres:

class InterviewViewSchema(ma.Schema):
    # nested schemas:

    class Meta:
        fields = (
            "id",
            "application_id",
            "interviewer_id",
            "interview_datetime",
            "length_mins",
            "format",
        )


# single interview schema, when one interview needs to be retrieved
interview_view_schema = InterviewViewSchema()
# multiple interviews schema, when many interviews need to be retrieved
interviews_view_schema = InterviewViewSchema(many=True)

