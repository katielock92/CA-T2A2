from main import db, ma

from marshmallow import fields

class Scorecard(db.Model):
    __tablename__ = "scorecards"

    id = db.Column(db.Integer, primary_key=True)
    scorecard_datetime = db.Column(db.DateTime, nullable=False)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    rating = db.Column(db.String, nullable=False)

    # add child relationship with Interviews:
    interviews = db.relationship("Interview", back_populates="scorecards")


# create the Scorecard Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class ScorecardSchema(ma.Schema):

    # field validations:
    # add a one of validation for rating
    class Meta:
        fields = (
            "id",
            "scorecard_datetime",
            "interview_id",
            "application_id",
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
    
# add some more nested schemas for scorecard here

    class Meta:
        fields = (
            "id",
            "scorecard_datetime",
            "interview",
            "notes",
            "rating"
        )


# single scorecard schema, when one scorecard needs to be retrieved
scorecard_view_schema = ScorecardViewSchema()
# multiple scorecards schema, when many scorecards need to be retrieved
scorecards_view_schema = ScorecardViewSchema(many=True)