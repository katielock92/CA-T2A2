from main import db, ma

from marshmallow import fields, validates
from marshmallow.validate import Length, And, Regexp, OneOf
from marshmallow.exceptions import ValidationError

VALID_FORMATS = ("Phone", "Video call")

class Interview(db.Model):
    __tablename__= "INTERVIEWS"

    id = db.Column(db.Integer,primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    interview_date = db.Column(db.DATETIME)
    length_mins = db.Column(db.Integer)
    format = db.Column(db.String())

    # add relationships here, examples:
        #user = db.relationship('User', back_populates='cards')
        #comments = db.relationship('Comment', back_populates='card', cascade='all, delete')
    


#create the Application Schema with Marshmallow, it will provide the serialisation needed for converting the data into JSON
class InterviewSchema(ma.Schema):
    # add nested info first, examples:
        #user = fields.Nested('UserSchema', only=['name', 'email'])
        #comments = fields.List(fields.Nested('CommentSchema'), exclude=['card'])
 
    format = fields.String(validate=OneOf(VALID_FORMATS))

    # add any other field validations

    class Meta:
        # Fields to expose
        fields = ("id", "") #add other fields

#single interview schema, when one interviews needs to be retrieved
interview_schema = InterviewSchema()
#multiple interviews schema, when many interviews need to be retrieved
interviews_schema = InterviewSchema(many=True)