from main import db, bcrypt
from models.jobs import Job
from models.users import User
from models.applications import Application
from models.interviews import Interview
from models.scorecards import Scorecard

from flask import Blueprint
from datetime import date

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
    # add information here for what to seed and add to the database:

    # create the test User objects:
    users = [
        User(
            first_name="Elizabeth",
            last_name="Riley",
            phone_number="0478921643",
            email="elizabeth.riley@example.com",
            password=bcrypt.generate_password_hash("Kipper1977").decode("utf-8"),
            access_level="Recruiter",
        ),
        User(
            first_name="Irene",
            last_name="Ryan",
            phone_number="0478630399",
            email="irene.ryan@example.com",
            password=bcrypt.generate_password_hash("Turtle76").decode("utf-8"),
            access_level="Hiring Manager",
        ),
        User(
            first_name="Maurice",
            last_name="Bailey",
            phone_number="0432043448",
            email="maurice.bailey@example.com",
            password=bcrypt.generate_password_hash("Namaste55").decode("utf-8"),
            access_level="Candidate",
        ),
        User(
            first_name="Regina",
            last_name="Taylor",
            phone_number="0475319599",
            email="regina.taylor@example.com",
            password=bcrypt.generate_password_hash("Camden123").decode("utf-8"),
            access_level="Recruiter"
        ),
        User(
            first_name="Ray",
            last_name="Torres",
            phone_number="0459459728",
            email="ray.torres@example.com",
            password=bcrypt.generate_password_hash("Hughes92").decode("utf-8"),
            access_level="Hiring Manager",
        ),
        User(
            first_name="Alfred",
            last_name="Campbell",
            phone_number="0432484967",
            email="alfred.campbell@example.com",
            password=bcrypt.generate_password_hash("Tetsuo43").decode("utf-8"),
            access_level="Candidate",
        )    
    ]
    db.session.add_all(users)

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
            hiring_manager_id=5,
        )
    ]
    db.session.add_all(jobs)

    db.session.commit()

    # create the test Application objects:
    applications = [
        Application(
            job_id=1,
            application_date=date.today(),
            candidate_id=3,
            location="Sydney",
            working_rights="Citizen",
            notice_period="2 weeks",
            salary_expectations=135000,
        ),
        Application(
            job_id="2",
            application_date=date.today(),
            candidate_id="6",
            location="Sydney",
            working_rights="Citizen",
            notice_period="4 weeks",
            salary_expectations=152000,
        )
    ]
    db.session.add_all(applications)

    db.session.commit()

    # create the test Interview objects:
    interviews = [
        Interview(
            application_id=1,
            interview_datetime="2023-07-21 10:30:00",
            length_mins=20,
            format="Phone",
            interviewer_id=1
        ),
        Interview(
            application_id=2,
            interview_datetime="2023-07-25 14:00:00",
            length_mins=45,
            format="Video call",
            interviewer_id=2
        ),
        Interview(
            application_id=2,
            interview_datetime="2023-07-23 10:30:00",
            length_mins=20,
            format="Phone",
            interviewer_id=1
        ),
    ]
    db.session.add_all(interviews)

    db.session.commit()


    # create the test Scorecard objects:
    scorecards = [
        Scorecard(
            interview_id=1,
            notes="Suitable candidate, fits what we're looking for. Proceed to HM interview.",
            rating=True,
        )
    ]
    db.session.add_all(scorecards)

    db.session.commit()

    print("Database tables seeded")
