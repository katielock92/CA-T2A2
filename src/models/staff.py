from main import db, ma

from marshmallow import fields
from marshmallow.validate import Regexp, And, Length



class Staff(db.Model):
    __tablename__ = "staff"

    # columns for the Staff table:
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50))
    admin = db.Column(db.Boolean, default=False, nullable=False)
    
    

    # adding parent relationship with Jobs and Interviews, does not cascade delete:
    jobs = db.relationship("Job", back_populates="hiring_manager")
    interviews = db.relationship("Interview", back_populates="interviewer")

    # adding child relationship with Users:
    user = db.relationship("User", back_populates="staff")


# creating a Schema with Marshmallow to allow us to serialise Users into JSON:
class StaffSchema(ma.Schema):
    # field validations:
    # validations not working as expected, revisit these
    name = fields.String(validate=And(Length(max=100, error="Name can only be a maximum of 100 characters long"),Regexp("^[a-zA-Z -]+",error="Name can contain only letters, spaces and hyphens - please try again.")))
    

    class Meta:
        fields = (
            "id",
            "user_id",
            "name",
            "title",
            "admin"
        )
        ordered = True


# defining the schema for when a single user needs to be retrieved:
staff_schema = StaffSchema()

# defining the schema for when multiple users need to be retrieved:
staffs_schema = StaffSchema(many=True)
