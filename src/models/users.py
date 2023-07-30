from main import db, ma

from marshmallow import fields
from marshmallow.validate import Length, Regexp


class User(db.Model):
    """Creates the User model in our database.

    Database columns:
        id: A required integer that is automatically serialised, a unique identifier for each user.
        email: A required string, unique to each user and required for login.
        password: A required string, encrypted using Bcrypt and used to authenticate a user on login.

    Database relationships:
        candidates: A child of Users, the user.id is a foreign key in the Candidates table.
        staff: A child of Users, the user.id is a foreign key in the Staff table.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    candidates = db.relationship(
        "Candidate", back_populates="user", cascade="all, delete"
    )
    staff = db.relationship("Staff", back_populates="user", cascade="all, delete")


class UserSchema(ma.Schema):

    """The primary Schema for the Users model.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used to load and update values in the Users table, but is not returned to users.

    Field validations:
        email: A regular expression is used to ensure that a correct email format is provided.
        password: A minimum length of 8 characters is required.

    Class meta: Includes all fields from the model.

    Schema variables:
        user_schema: When a single User record is accessed.
        users_schema: When multiple User records are accessed.

    """

    email = fields.String(
        validate=Regexp(
            "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            error="Invalid email address, please try again",
        )
    )
    password = fields.String(
        validate=Length(min=8), error="Password must be at least 8 characters"
    )

    class Meta:
        fields = ("id", "email", "password")
        ordered = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserViewSchema(ma.Schema):

    """A secondary Schema for the Users model for returning data to users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data to display to the user, as not all fields are returned.

    Field validations: Same as User_Schema.

    Class meta: Includes the id and email fields, password is excluded.

    Schema variables:
        user_view_schema: When a single User record is accessed.
        users_view_schema: When multiple User records are accessed.

    """

    email = fields.String(
        validate=Regexp(
            "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
            error="Invalid email address, please try again",
        )
    )
    password = fields.String(
        validate=Length(min=8), error="Password must be at least 8 characters"
    )

    class Meta:
        fields = ("id", "email")
        ordered = True


user_view_schema = UserViewSchema()
users_view_schema = UserViewSchema(many=True)
