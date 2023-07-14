from main import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp, OneOf


VALID_ACCESS = ("Candidate", "Hiring Manager", "Recruiter")


class User(db.Model):
    __tablename__ = "users"

    # columns for the User table:
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String)
    access_level = db.Column(db.String, default="Candidate")

    # adding parent relationship with Jobs for HM users, does not cascade delete:
    jobs = db.relationship("Job", back_populates="hiring_manager")

    # adding parent relationship with Applications for Candidate users, add cascade delete later:
    applications = db.relationship("Application", back_populates="candidate")


# creating a Schema with Marshmallow to allow us to serialise Users into JSON:
class UserSchema(ma.Schema):

    # field validations:
    email = fields.String(
        required=True,
        validate=Regexp(
            "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+",
            error="Invalid email format please try again.",
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
