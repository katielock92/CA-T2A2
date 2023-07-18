from main import db, bcrypt
from models.users import User, user_schema

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from psycopg2 import errorcodes
from datetime import timedelta

auth = Blueprint("auth", __name__, url_prefix="/auth")

# POST method for new users to register:
@auth.route("/register", methods=["POST"])
def auth_register():
    try:
        body_data = request.get_json()
        user = User()
        user.first_name = body_data.get("first_name")
        user.last_name = body_data.get("last_name")
        user.phone_number = body_data.get("phone_number") # need to add validation
        user.email = body_data.get("email") # need to add email format validation
        if body_data.get("password"):
            user.password = bcrypt.generate_password_hash(
                body_data.get("password")
            ).decode("utf-8")
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
    except ValidationError:
        return {"error": f"Invalid format, please try again."}, 409
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email address already in use, please login or register with a different email."}, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The '{err.orig.diag.column_name}' field is required, please try again."}, 409
        

# POST method for existing users to login:
@auth.route("/login", methods=["POST"])
def auth_login():
    body_data = request.get_json()
    stmt = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(days=1)
        )
        return {"email": user.email, "token": token}
    else:
        return {"error": "Invalid email or password"}, 401
