from main import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp, And, Length


class Candidate(db.Model):
    __tablename__ = "candidates"

    # columns for the Candidate table:
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    # string used for phone number so that leading zeroes aren't dropped and certain special characters are allowed:
    phone_number = db.Column(db.String(20), nullable=False)

    # adding parent relationship with Applications and Interviews:
    applications = db.relationship(
        "Application", back_populates="candidate"
    )  # cascade="all, delete"
    interviews = db.relationship(
        "Interview", back_populates="candidate"
    )  # cascade="all, delete"

    # adding child relationship with Users:
    user = db.relationship("User", back_populates="candidates")


# creating a Schema with Marshmallow to allow us to serialise Candidates into JSON:
class CandidateSchema(ma.Schema):
    # field validations:
    name = fields.String(
        required=True,
        validate=And(
            Length(max=100, error="Name can only be a maximum of 100 characters long"),
            Regexp(
                "^[a-zA-Z -]+",
                error="Name can contain only letters, spaces and hyphens - please try again.",
            ),
        ),
    )
    phone_number = fields.String(
        required=True,
        validate=And(
            Length(
                min=10, error="Phone number must be between 10-20 characters in length"
            ),
            Length(
                max=20, error="Phone number must be between 10-20 characters in length"
            ),
            Regexp(
                "^[0-9() -+]+",
                error="Phone number can only contains numbers and certain special characters - please try again.",
            ),
        ),
    )

    class Meta:
        fields = ("id", "user_id", "name", "phone_number")
        ordered = True


candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)
