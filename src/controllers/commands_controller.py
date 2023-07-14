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
            hiring_manager_id="2",
        )
    ]
    db.session.add_all(jobs)

    db.session.commit()

    # create the test Application objects:
    applications = [
        Application(
            job_id="1",
            application_date=date.today(),
            candidate_id="3",
            location="Sydney",
            working_rights="Citizen",
            notice_period="2 weeks",
            salary_expectations=135000,
        )
    ]
    db.session.add_all(applications)

    db.session.commit()

    # create the test Interview objects:
    interviews = [
        Interview(
            application_id="1",
            interview_date="2023-07-21",
            length_mins=20,
            format="Phone",
        )
    ]
    db.session.add_all(interviews)

    db.session.commit()


    # create the test Scorecard objects:
    scorecards = [
        Scorecard(
            interview_id="1",
            notes="Suitable candidate, fits what we're looking for. Proceed to HM interview.",
            rating=True,
        )
    ]
    db.session.add_all(scorecards)

    db.session.commit()

    print("Database tables seeded")
