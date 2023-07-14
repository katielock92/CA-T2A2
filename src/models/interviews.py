from main import db, ma

from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

VALID_FORMATS = ("Phone", "Video call")


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("applications.id"))  # add nullable later
    interview_date = db.Column(db.String)  # add date format later
    length_mins = db.Column(db.Integer)
    format = db.Column(db.String())

    # adding parent relationship with Scorecards, add cascade later
    scorecards = db.relationship("Scorecard", back_populates="interviews")

    # add child relationship with Applications:
    application = db.relationship("Application", back_populates="interviews")


# create the Interview Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class InterviewSchema(ma.Schema):
    # nested schemas:

    # field validations:
    format = fields.String(validate=OneOf(VALID_FORMATS))

    class Meta:
        fields = (
            "id",
            "application_id",
            "interview_date",
            "length_mins",
            "format",
        )  # add other fields


# single interview schema, when one interview needs to be retrieved
interview_schema = InterviewSchema()
# multiple interviews schema, when many interviews need to be retrieved
interviews_schema = InterviewSchema(many=True)
