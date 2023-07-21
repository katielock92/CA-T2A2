from main import db, ma

from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(), default="Open", nullable=False)
    salary_budget = db.Column(db.Integer(), nullable=False)
    hiring_manager_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)

    # adding child relationship with Staff:
    hiring_manager = db.relationship("Staff", back_populates="jobs")

    # adding parent relationship with Applications:
    applications = db.relationship(
        "Application", back_populates="job", cascade="all, delete"
    )


# field validations for schemas:
VALID_STATUSES = ("Open", "Closed")

validate_title = fields.String(
    required=True,
    validate=And(
        Length(min=4, error="Job title must be at least 4 characters long"),
        Length(max=100, error="Job title can only be a maximum of 100 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+",
            error="Title must contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)

validate_department = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Department must be at least 2 characters long"),
        Length(max=50, error="Department can only be a maximum of 50 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+",
            error="Department must contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)
validate_location = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Location must be at least 2 characters long"),
        Length(max=50, error="Location can only be a maximum of 50 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+",
            error="Location name must contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)


# creating a primary Schema with Marshmallow to allow us to serialise Jobs into JSON:
class JobSchema(ma.Schema):
    # field validations:
    title = validate_title
    department = validate_department
    location = validate_location
    description = fields.String(required=True)
    salary_budget = fields.Integer(required=True)
    hiring_manager_id = fields.Integer(required=True)
    status = fields.String(validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = (
            "id",
            "title",
            "department",
            "location",
            "description",
            "hiring_manager_id",
            "status",
            "salary_budget",
        )
        ordered = True


job_schema = JobSchema()
jobs_schema = JobSchema(many=True)


# additional Schema for displaying jobs to authorised staff who can see budget:
class JobAdminSchema(ma.Schema):
    # nested schemas:
    hiring_manager = fields.Nested("StaffSchema", only=["name", "title"])

    # field validations:
    title = validate_title
    department = validate_department
    location = validate_location
    description = fields.String(required=True)
    salary_budget = fields.Integer(required=True)
    hiring_manager_id = fields.Integer(required=True)
    status = fields.String(required=True, validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = (
            "id",
            "title",
            "department",
            "location",
            "description",
            "hiring_manager",
            "status",
            "salary_budget",
        )
        ordered = True


job_admin_schema = JobAdminSchema()
jobs_admin_schema = JobAdminSchema(many=True)


# additional Schema for displaying jobs to authorised staff who can't see budget:
class JobStaffSchema(ma.Schema):
    # nested schemas:
    hiring_manager = fields.Nested("StaffSchema", only=["name", "title"])

    # field validations:
    title = validate_title
    department = validate_department
    location = validate_location
    description = fields.String(required=True)
    hiring_manager_id = fields.Integer(required=True)
    status = fields.String(required=True, validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = (
            "id",
            "title",
            "department",
            "location",
            "description",
            "hiring_manager",
            "status",
        )
        ordered = True


job_staff_schema = JobStaffSchema()
jobs_staff_schema = JobStaffSchema(many=True)


# additional Schema for displaying jobs to non-authenticated users:
class JobViewSchema(ma.Schema):
    # field validations:
    title = validate_title
    department = validate_department
    location = validate_location
    description = fields.String(required=True)
    status = fields.String(required=True, validate=OneOf(VALID_STATUSES))

    class Meta:
        fields = ("id", "title", "department", "location", "description", "status")
        ordered = True


job_view_schema = JobViewSchema()
jobs_view_schema = JobViewSchema(many=True)
