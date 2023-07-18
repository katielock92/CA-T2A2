from main import db, ma

from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

class Scorecard(db.Model):
    __tablename__ = "scorecards"

    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"))  # add nullable later
    #interviewer_id - add later with relation
    notes = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Boolean, nullable=False)
    # add rest of the fields

    # add child relationship with Interviews:
    interviews = db.relationship("Interview", back_populates="scorecards")


# create the Scorecard Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class ScorecardSchema(ma.Schema):
    # nested schemas:

    # field validations:

    class Meta:
        fields = (
            "id",
            "interview_id",
            "interviewer_id",
            "notes",
            "rating"
        )  # add other fields


# single scorecard schema, when one scorecard needs to be retrieved
scorecard_schema = ScorecardSchema()
# multiple scorecards schema, when many scorecards need to be retrieved
scorecards_schema = ScorecardSchema(many=True)
