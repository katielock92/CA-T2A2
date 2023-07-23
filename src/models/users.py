from main import db, ma

from marshmallow import fields
from marshmallow.validate import Length, Regexp


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


# creating a primary Schema with Marshmallow to allow us to serialise Users into JSON:
class UserSchema(ma.Schema):
    # field validations:
    email = fields.String(validate=Regexp(
                "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                error="Invalid email address, please try again",
            ))
    password = fields.String(validate=Length(min=8), error="Password must be at least 8 characters")

    class Meta:
        fields = ("id", "email", "password")
        ordered = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)

# creating a primary Schema with Marshmallow to allow us to serialise Users into JSON:
class UserViewSchema(ma.Schema):
    # field validations:
    email = fields.String(validate=Regexp(
                "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                error="Invalid email address, please try again",
            ))
    password = fields.String(validate=Length(min=8), error="Password must be at least 8 characters")

    class Meta:
        fields = ("id", "email")
        ordered = True


user_view_schema = UserViewSchema()
users_view_schema = UserViewSchema(many=True)
