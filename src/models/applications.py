from main import db, ma

from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

VALID_STATUSES = ("To review", "Recruiter interview", "Manager interview", "Offer", "Rejected")

class Application(db.Model):
    __tablename__= "applications"

    id = db.Column(db.Integer,primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    application_date = db.Column(db.DATETIME)
    status = db.Column(db.String(), default="To review")
    #applicant user id
    location = db.Column(db.String(50))
    working_rights = db.Column(db.String(100))
    notice_period = db.Column(db.String(50))
    salary_expectations = db.Column(db.Integer()) # need to find SQL type for money if possible
    #resume
    #cover letter

    # add relationships here, examples:
    #job = db.relationship("Job", back_populates="applications", cascade="all, delete")
    


#create the Application Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class ApplicationSchema(ma.Schema):
    # add nested info first, examples:
        #user = fields.Nested('UserSchema', only=['name', 'email'])
        #comments = fields.List(fields.Nested('CommentSchema'), exclude=['card'])
 
    status = fields.String(validate=OneOf(VALID_STATUSES))

    # add any other field validations

    class Meta:
        # Fields to expose
        fields = ("id", "job_id", "application_date", "status", "location", "working_rights", "notice_period", "salary_expectations") #add other fields

#single application schema, when one applications needs to be retrieved
application_schema = ApplicationSchema()
#multiple application schema, when many applications need to be retrieved
applications_schema = ApplicationSchema(many=True)