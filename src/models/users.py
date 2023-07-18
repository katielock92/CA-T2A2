from main import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp, OneOf, And, Length


VALID_ACCESS = ("Candidate", "Hiring Manager", "Recruiter")


class User(db.Model):
    __tablename__ = "users"

    # columns for the User table:
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # string used for phone number so that leading zeroes aren't dropped and certain special characters are allowed:
    password = db.Column(db.String(), nullable=False)
    access_level = db.Column(db.String, default="Candidate", nullable=False)

    # adding parent relationship with Jobs, Interviews and Scorecards, does not cascade delete:
    jobs = db.relationship("Job", back_populates="hiring_manager")
    interviews = db.relationship("Interview", back_populates="interviewer")
    scorecards = db.relationship("Scorecard", back_populates="interviewer")

    # adding parent relationship with Applications for Candidate users:
    applications = db.relationship(
        "Application", back_populates="candidate", cascade="all, delete"
    )


# creating a Schema with Marshmallow to allow us to serialise Users into JSON:
class UserSchema(ma.Schema):
    # field validations:
    # validations not working as expected, revisit these
    email = fields.String(
        validate=Regexp(
            "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
            error="Invalid email format - please try again.",
        ),
    )
    first_name = fields.String(
        validate=And(
            Length(
                max=50, error="First name can only be a maximum of 50 characters long"
            ),
            Regexp(
                "^[a-zA-Z -]+",
                error="Name can contain only letters, spaces and hyphens - please try again.",
            ),
        ),
    )
    last_name = fields.String(
        validate=And(
            Length(
                max=50, error="Last name can only be a maximum of 50 characters long"
            ),
            Regexp(
                "^[a-zA-Z -]+",
                error="Name can contain only letters, spaces and hyphens - please try again.",
            ),
        ),
    )
    phone_number = fields.String(
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
    access_level = fields.String(validate=OneOf(VALID_ACCESS))

    class Meta:
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password",
            "access_level",
        )
        ordered = True


# defining the schema for when a single user needs to be retrieved:
user_schema = UserSchema(exclude=["password"])

# defining the schema for when multiple users need to be retrieved:
users_schema = UserSchema(many=True, exclude=["password"])
