from main import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp, And, Length


class Candidate(db.Model):

    """Creates the Candidate model in our database.

    Database columns:
        id: A required integer that is automatically serialised, a unique identifier for each candidate.
        user_id: A required integer, a unique foreign key that links the candidate record to the Users table.
        name: A required string, contain the Candidate's full name.
        phone_number: A required string, contains the Candidate's phone number. A string is used rather than an integer so that a leading 0 is not dropped.

    Database relationships:
        applications: A child of Candidates, the candidate.id is a foreign key in the Applications table.
        interviews: A child of Candidates, the candidate.id is a foreign key in the Interviews table.
        users: A parent of Candidates, the user.id is a foreign key in the Candidates table.
    """

    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    applications = db.relationship(
        "Application", back_populates="candidate", cascade="all, delete"
    )
    interviews = db.relationship(
        "Interview", back_populates="candidate", cascade="all, delete"
    )
    user = db.relationship("User", back_populates="candidates")

class CandidateSchema(ma.Schema):

    """The Schema for the Candidates model.

    Allows us to serialise into JSON using Marshmallow.
    No additional schemas for this model.

    Field validations:
        name: A regular expression is used so that only letters, spaces and hyphens can be used. The maximum field length is 100 characters.
        phone_number: A regular expression is used so that only numbers, spaces, hyphens and brackets can be used. Field length has a min of 10 and max of 20 characters.

    Class meta: Includes all fields from the model.

    Schema variables:
        candidate_schema: When a single Candidate record is accessed.
        candidates_schema: When multiple Candidates records are accessed.

    """

    name = fields.String(
        required=True,
        validate=And(
            Length(max=100, error="Name can only be a maximum of 100 characters long"),
            Regexp(
                "^[a-zA-Z -]+$",
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
