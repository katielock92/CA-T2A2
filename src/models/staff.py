from main import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp, And, Length


class Staff(db.Model):

    """Creates the Staff model in our database.

    Database columns:
        id: A required integer that is automatically serialised, a unique identifier for each staff.
        user_id: A required integer, a unique foreign key that links the staff record to the Users table.
        name: A required string, contain the Staff member's full name.
        title: A required string, contains the Staff member's job title.
        admin: A boolean that specifies if the Staff user has Admin permissions. Defaults to False.

    Database relationships:
        jobs: A child of Staff, the staff.id is a foreign key in the Jobs table.
        interviews: A child of Staff, the staff.id is a foreign key in the Interviews table.
        users: A parent of Staff, the user.id is a foreign key in the Staff table.
    """

    __tablename__ = "staff"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    jobs = db.relationship("Job", back_populates="hiring_manager")
    interviews = db.relationship("Interview", back_populates="interviewer")
    user = db.relationship("User", back_populates="staff")


class StaffSchema(ma.Schema):

    """The Schema for the Staff model.

    Allows us to serialise into JSON using Marshmallow.
    No additional schemas for this model.

    Field validations:
        name: A regular expression is used so that only letters, spaces and hyphens can be used. The maximum field length is 100 characters.
        title: A regular expression is used so that only letters, numbers, spaces and certain special characters can be used. The field length has a min of 4 and max of 50 characters.
        user_id: A required field, integer format.
        admin: A required field, boolean format.

    Class meta: Includes all fields from the model.

    Schema variables:
        staff_schema: When a single Staff record is accessed.
        staffs_schema: When multiple Staff records are accessed.

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
    user_id = fields.Integer(required=True)
    title = fields.String(
        required=True,
        validate=And(
            Length(min=4, error="Title must be at least 4 characters long"),
            Length(max=50, error="Title can only be a maximum of 50 characters long"),
            Regexp(
                "^[a-zA-Z0-9 -()]+$",
                error="Title can contain only letters, numbers and certain special characters - please try again.",
            ),
        ),
    )
    admin = fields.Boolean(required=True)

    class Meta:
        fields = ("id", "user_id", "name", "title", "admin")
        ordered = True


staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)
