from main import db, ma

from marshmallow import fields
from marshmallow.validate import Email, Length


class User(db.Model):
    __tablename__ = "users"

    # columns for the User table:
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    # adding parent relationship with Candidates and Staff:
    candidates = db.relationship(
        "Candidate", back_populates="user", cascade="all, delete"
    )
    staff = db.relationship("Staff", back_populates="user", cascade="all, delete")


# creating a Schema with Marshmallow to allow us to serialise Users into JSON:
class UserSchema(ma.Schema):
    # field validations:
    email = fields.String(validate=Email)
    password = fields.String(validate=Length(min=8))

    class Meta:
        fields = ("id", "email", "password")
        ordered = True


user_schema = UserSchema(exclude=["password"])
users_schema = UserSchema(many=True, exclude=["password"])
