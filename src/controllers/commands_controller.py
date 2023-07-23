from main import db, bcrypt
from models.jobs import Job
from models.users import User
from models.candidates import Candidate
from models.staff import Staff
from models.applications import Application
from models.interviews import Interview
from models.scorecards import Scorecard

from flask import Blueprint
from datetime import date, datetime

db_commands = Blueprint("db", __name__)


# Command to create the database tables:
@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Database tables created")


# Command to drop the database tables:
@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Database tables dropped")


# Commands to seed the database tables:
@db_commands.cli.command("seed")
def seed_db():

    # create the test User objects:
    users = [
        User(
            email="elizabeth.riley@example.com",
            password=bcrypt.generate_password_hash("Kipper1977").decode("utf-8"),
        ),
        User(
            email="irene.ryan@example.com",
            password=bcrypt.generate_password_hash("Turtle76").decode("utf-8"),
        ),
        User(
            email="maurice.bailey@example.com",
            password=bcrypt.generate_password_hash("Namaste55").decode("utf-8"),
        ),
        User(
            email="regina.taylor@example.com",
            password=bcrypt.generate_password_hash("Camden123").decode("utf-8"),
        ),
        User(
            email="ray.torres@example.com",
            password=bcrypt.generate_password_hash("Hughes92").decode("utf-8"),
        ),
        User(
            email="alfred.campbell@example.com",
            password=bcrypt.generate_password_hash("Tetsuo43").decode("utf-8"),
        ),
    ]
    db.session.add_all(users)

    db.session.commit()

    # create the test Staff and Candidate objects:

    staff = [
        Staff(name="Elizabeth Riley", user_id=1, title="Recruiter", admin=True),
        Staff(name="Irene Ryan", user_id=2, title="Engineering Manager", admin=False),
        Staff(name="Regina Taylor", user_id=4, title="Recruiter", admin=True),
        Staff(name="Ray Torres", user_id=5, title="VP, Sales", admin=False),
    ]

    db.session.add_all(staff)

    candidates = [
        Candidate(name="Maurice Bailey", user_id=3, phone_number="0432043448"),
        Candidate(name="Alfred Campbell", user_id=6, phone_number="0432484967"),
    ]

    db.session.add_all(candidates)
    db.session.commit()

    # create the test Job objects:
    jobs = [
        Job(
            title="DevOps Engineer",
            description="We're looking for someone who's keen to learn and grow with us in the Site Reliability Engineering/DevOps space. Using a best in class AWS stack centred around Kubernetes (EKS) and Go microservices, CI/CD driven, and using great tools like Terraform, join a team that makes a true impact.",
            department="Engineering",
            location="Australia (Remote)",
            status="Open",
            salary_budget=140000,
            hiring_manager_id=2,
        ),
        Job(
            title="Account Director",
            description="In this exciting role, you'll be engaging with senior executives at multiple levels and functions across the client organisation. Your experience working across complex and/or matrix level organisations will serve you well in understanding the complexity and dynamics of working with these companies.",
            department="Accounts",
            location="Sydney",
            status="Open",
            salary_budget=150000,
            hiring_manager_id=4,
        ),
    ]
    db.session.add_all(jobs)

    db.session.commit()

    # create the test Application objects:
    applications = [
        Application(
            job_id=1,
            application_date=date.today(),
            candidate_id=1,
            location="Sydney",
            working_rights="Citizen",
            notice_period="2 weeks",
            salary_expectations=135000,
            resume="https://www.docdroid.net/WyjIuyO/fake-resume-pdf",
        ),
        Application(
            job_id=2,
            application_date=date.today(),
            candidate_id=2,
            location="Sydney",
            working_rights="Citizen",
            notice_period="4 weeks",
            salary_expectations=152000,
            resume="https://www.docdroid.net/WyjIuyO/fake-resume-pdf",
        ),
    ]
    db.session.add_all(applications)

    db.session.commit()

    # create the test Interview objects:
    interviews = [
        Interview(
            application_id=1,
            candidate_id=1,
            interview_datetime="2023-07-21 10:30:00",
            length_mins=20,
            format="Phone",
            interviewer_id=1,
        ),
        Interview(
            application_id=1,
            candidate_id=1,
            interview_datetime="2023-07-25 14:00:00",
            length_mins=45,
            format="Video call",
            interviewer_id=2,
        ),
        Interview(
            application_id=2,
            candidate_id=2,
            interview_datetime="2023-07-23 10:30:00",
            length_mins=20,
            format="Phone",
            interviewer_id=1,
        ),
    ]
    db.session.add_all(interviews)

    db.session.commit()

    # create the test Scorecard objects:
    scorecards = [
        Scorecard(
            scorecard_datetime=datetime.now(),
            interview_id=1,
            notes="Good candidate, fits what we're looking for and seems to be a culture fit. Proceed to next interview.",
            rating="Yes",
        )
    ]
    db.session.add_all(scorecards)

    db.session.commit()

    print("Database tables seeded")
