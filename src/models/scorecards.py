from main import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf


class Scorecard(db.Model):

    """Creates the Scorecard model in our database.

    Database columns:
        id: A required integer that is automatically serialised, a unique identifier for each scorecard.
        interview_id: A required integer, a foreign key that links to the Interviews table.
        scorecard_datetime: A required datetime field, uses the DateTime module to record the date and time the scorecard record is created.
        notes: A required text field, for the interviewer to document their notes and thoughts on how the interview went.
        rating: A required string field, for the interviewer to rate the candidates's interview.

    Database relationships:
        interviews: A parent of Scorecards, the interview.id is a foreign key in the Scorecards table.
    """

    __tablename__ = "scorecards"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(
        db.Integer, db.ForeignKey("interviews.id"), unique=True, nullable=False
    )
    scorecard_datetime = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    rating = db.Column(db.String, nullable=False)

    interview = db.relationship("Interview", back_populates="scorecards")


class ScorecardSchema(ma.Schema):

    """The primary Schema for the Scorecards model.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used to load and update values in the Scorecards table, but is not returned to users.

    Field validations:
        scorecard_datetime: Uses the ISO datetime format of YYYY-MM-DD HH:DDAM
        notes: A required field, text format.
        rating: Only accepts input that matches a specified list of values.

    Class meta: Includes all fields from the model.

    Schema variables:
        scorecard_schema: When a single Scorecard record is accessed.

    """

    scorecard_datetime = fields.DateTime(format="%Y-%m-%d %H:%M%p")
    notes = fields.String(required=True)
    rating = fields.String(
        required=True,
        validate=OneOf("Strong Yes", "Yes", "No Decision", "No", "Strong No"),
    )

    class Meta:
        fields = ("id", "scorecard_datetime", "interview_id", "notes", "rating")


scorecard_schema = ScorecardSchema()


class ScorecardViewSchema(ma.Schema):

    """Additional Schema for the Scorecards model for Staff users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data from the Scorecards model to authenticated Staff users.

    Nested schemas: interview is a nested schema from the InterviewScorecardSchema, which displays the candidate's name, the interviewer's name and title, and is linked via the interview_id foreign key field.

    Field validations: Same as ScorecardSchema.

    Class meta: Includes all fields from the model except interview_id, which is replaced with the interview nested schema.

    Schema variables:
        scorecard_view_schema: When a single Scorecard record is accessed.

    """

    interview = fields.Nested("InterviewScorecardSchema")

    scorecard_datetime = fields.DateTime(format="%Y-%m-%d %H:%M%p")
    notes = fields.String(required=True)
    rating = fields.String(
        required=True,
        validate=OneOf("Strong Yes", "Yes", "No Decision", "No", "Strong No"),
    )

    class Meta:
        fields = ("id", "interview", "scorecard_datetime", "notes", "rating")


scorecard_view_schema = ScorecardViewSchema()
