from main import db, ma

from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

class Scorecard(db.Model):
    __tablename__ = "scorecards"

    id = db.Column(db.Integer, primary_key=True)
    scorecard_datetime = db.Column(db.DateTime, nullable=False)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)
    interviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    notes = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Boolean, nullable=False)

    # add child relationship with Interviews and Users:
    interviews = db.relationship("Interview", back_populates="scorecards")
    interviewer = db.relationship("User", back_populates="scorecards")


# create the Scorecard Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class ScorecardSchema(ma.Schema):

    # field validations:

    class Meta:
        fields = (
            "id",
            "scorecard_datetime",
            "interview_id",
            "application_id",
            "interviewer_id",
            "notes",
            "rating"
        )


# single scorecard schema, when one scorecard needs to be retrieved
scorecard_schema = ScorecardSchema()
# multiple scorecards schema, when many scorecards need to be retrieved
scorecards_schema = ScorecardSchema(many=True)

# additional Schema for displaying scorecards to authenticated staff:
class ScorecardViewSchema(ma.Schema):
    # nested schemas:
    interviewer = fields.Nested(
        "UserSchema", only=["first_name", "last_name", "email"]
    )
# add some more nested schemas for scorecard here

    class Meta:
        fields = (
            "id",
            "scorecard_datetime",
            "interview",
            "interviewer",
            "notes",
            "rating"
        )


# single scorecard schema, when one scorecard needs to be retrieved
scorecard_view_schema = ScorecardViewSchema()
# multiple scorecards schema, when many scorecards need to be retrieved
scorecards_view_schema = ScorecardViewSchema(many=True)