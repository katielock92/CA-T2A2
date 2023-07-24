from main import db, ma

from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

class Scorecard(db.Model):
    __tablename__ = "scorecards"

    id = db.Column(db.Integer, primary_key=True)
    scorecard_datetime = db.Column(db.DateTime, nullable=False)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    rating = db.Column(db.String, nullable=False)

    # add child relationship with Interviews:
    interviews = db.relationship("Interview", back_populates="scorecards")

# field validations for schemas:
VALID_STATUSES = ("Strong Yes", "Yes", "No Decision", "No", "Strong No")


# create the Scorecard Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class ScorecardSchema(ma.Schema):

    # field validations:
    interview_id = fields.Integer(required=True)
    scorecard_datetime = fields.DateTime(format="%Y-%m-%d %H:%M%p")
    notes = fields.String(required=True)
    rating = fields.String(required=True, validate=OneOf(VALID_STATUSES))
    class Meta:
        fields = (
            "id",
            "scorecard_datetime",
            "interview_id",
            "notes",
            "rating"
        )


scorecard_schema = ScorecardSchema()
scorecards_schema = ScorecardSchema(many=True)

# additional Schema for displaying scorecards to authenticated staff:
class ScorecardViewSchema(ma.Schema):
    # nested schemas:
    interview = fields.Nested("InterviewStaffViewSchema")
    
    # field validations:
    interview_id = fields.Integer(required=True)
    scorecard_datetime = fields.DateTime(format="%Y-%m-%d %H:%M%p")
    notes = fields.String(required=True)
    rating = fields.String(required=True, validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = (
            "id",
            "scorecard_datetime",
            "interview_id",
            "interview",
            "notes",
            "rating"
        )


scorecard_view_schema = ScorecardViewSchema()
scorecards_view_schema = ScorecardViewSchema(many=True)