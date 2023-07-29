from main import db, ma

from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf


class Job(db.Model):

    """Creates the Job model in our database.

    Database columns:
        id: A required integer that is automatically serialised, a unique identifier for each job.
        title: A required string, the title of the job being advertised.
        description: A required text field, a description of the job responsibilities and requirements.
        location: A required string, the location of where this job is based.
        status: A required string, specifies if the job listing is currently open or has been closed.
        salary_budget: A required integer, the budget for the role's salary.
        hiring_manager_id: A required integer, a foreign key that links to the Staff table for the hiring manager.

    Database relationships:
        applications: A child of Jobs, the job.id is a foreign key in the Applications table.
        staff: A parent of Jobs, the staff.id is a foreign key in the Jobs table.
    """

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(), default="Open", nullable=False)
    salary_budget = db.Column(db.Integer(), nullable=False)
    hiring_manager_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)

    hiring_manager = db.relationship("Staff", back_populates="jobs")
    applications = db.relationship(
        "Application", back_populates="job", cascade="all, delete"
    )


"""Field validations for the schemas.

Defined as variables outside of an individual schema as they are reused across multiple schemas.

"""

VALID_STATUSES = ("Open", "Closed")

validate_title = fields.String(
    required=True,
    validate=And(
        Length(min=4, error="Job title must be at least 4 characters long"),
        Length(max=100, error="Job title can only be a maximum of 100 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+$",
            error="Title can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)

validate_department = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Department must be at least 2 characters long"),
        Length(max=50, error="Department can only be a maximum of 50 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+$",
            error="Department can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)
validate_location = fields.String(
    required=True,
    validate=And(
        Length(min=2, error="Location must be at least 2 characters long"),
        Length(max=50, error="Location can only be a maximum of 50 characters long"),
        Regexp(
            "^[a-zA-Z0-9() -]+$",
            error="Location can contain only letters, numbers, spaces and certain special characters - please try again.",
        ),
    ),
)


class JobSchema(ma.Schema):

    """The primary Schema for the Jobs model.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used to load and update values in the Jobs table, but is not returned to users.

    Field validations:
        title: A regular expression is used so that only letters, numbers, spaces and certain special characters can be used. The field length has a min of 4 and max of 100 characters.
        department: A regular expression is used so that only letters, numbers, spaces and certain special characters can be used. The field length has a min of 2 and max of 50 characters.
        location: A regular expression is used so that only letters, numbers, spaces and certain special characters can be used. The field length has a min of 2 and max of 50 characters.
        description: A required field, text format.
        salary_budget: A required field, integer format.
        hiring_manager_id: A required field, integer format.
        status: Only accepts input that matches a specified list of values.

    Class meta: Includes all fields from the model.

    Schema variables:
        job_schema: When a single Job record is accessed.
        jobs_schema: When multiple Job records are accessed.

    """

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


class JobAdminSchema(ma.Schema):

    """Additional Schema for the Jobs model for Admin users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data from the Jobs model to authenticated Admin users.

    Nested schemas:
        hiring_manager is a nested schema from the StaffSchema, which displays the name and title fields of the Staff record linked via the hiring_manager_id foreign key field.

    Field validations: Same as Job_Schema.

    Class meta: Includes all fields from the model except hiring_manager_id, as a nested schema is used instead.

    Schema variables:
        job_admin_schema: When a single Job record is accessed.
        jobs_admin_schema: When multiple Job records are accessed.

    """

    hiring_manager = fields.Nested("StaffSchema", only=["name", "title"])

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


class JobStaffSchema(ma.Schema):

    """Additional Schema for the Jobs model for non-Admin Staff users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data from the Jobs model to authenticated Staff users who do not have Admin access.

    Nested schemas: hiring_manager is a nested schema from the StaffSchema, which displays the name and title fields of the Staff record linked via the hiring_manager_id foreign key field.

    Field validations: Same as Job_Schema.

    Class meta: Includes all fields from the model except:
    - hiring_manager_id, as a nested schema is used instead
    - salary_budget

    Schema variables:
        job_staff_schema: When a single Job record is accessed.
        jobs_staff_schema: When multiple Job records are accessed.

    """

    hiring_manager = fields.Nested("StaffSchema", only=["name", "title"])

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


class JobViewSchema(ma.Schema):

    """Additional Schema for the Jobs model for non-Staff users.

    Allows us to serialise into JSON using Marshmallow.
    This version of the schema is used when returning data from the Jobs model to users with no JWT or without Staff access.

    Field validations: Same as Job_Schema.

    Class meta: Includes all fields from the model except:
    - hiring_manager_id
    - salary_budget

    Schema variables:
        job_view_schema: When a single Job record is accessed.
        jobs_view_schema: When multiple Job records are accessed.

    """

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
