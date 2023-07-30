from main import db, bcrypt
from models.users import User, user_schema, user_view_schema
from models.staff import Staff

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes
from datetime import timedelta
import functools


# adding wrapper functions for authorised actions:
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            query = db.select(Staff).filter_by(user_id=user_id)
            user = db.session.scalar(query)
            if user.admin:
                return fn(*args, **kwargs)
            else:
                return {"error": "Not authorised to perform this action"}, 403
        except AttributeError:
            return {"error": "Not authorised to perform this action"}, 403

    return wrapper


def authorise_as_staff(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            query = db.select(Staff).filter_by(user_id=user_id)
            user = db.session.scalar(query)
            if user:
                return fn(*args, **kwargs)
            else:
                return {"error": "Not authorised to perform this action"}, 403
        except AttributeError:
            return {"error": "Not authorised to perform this action"}, 403

    return wrapper


auth = Blueprint("auth", __name__, url_prefix="/auth")


# POST method for new users to register:
@auth.route("/register", methods=["POST"])
def auth_register():
    """Creates new record in the Users table.

    A POST request is used to create a new record in the Users table, which is later used to authenticate the user.

    Args:
        None required.

    Input:
        Email and password, in JSON format.

    Returns:
        Key value pairs for the email and id fields for the new record in the Users table, in JSON format.

    Errors:
        xx: 
        409: Displayed if email field provided already exists in the Users table.
        409: Displayed if a required field is not provided.
    """
    try:
        body_data = user_schema.load(request.json)
        user = User()
        user.email = body_data["email"]
        user.password = bcrypt.generate_password_hash(body_data["password"]).decode("utf-8")
        db.session.add(user)
        db.session.commit()
        return user_view_schema.dump(user), 201
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {
                "error": "Email address already in use, please login or register with a different email."
            }, 409
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {
                "error": f"The '{err.orig.diag.column_name}' field is required, please try again."
            }, 409
        else:
            return {"error": "Uh oh! An unknown error occurred"}, 400


@auth.route("/login", methods=["POST"])
def auth_login():
    """Authenticates an existing record in the Users table.

    A POST request is used to authenticate a record in the Users table, and return a JWT that is used to perform other operations that require authentication.

    Args:
        None required.

    Input:
        Email and password, in JSON format.

    Returns:
        Key value pairs for the email field for the matching record in the Users table, and a token, in JSON format.

    Errors:
        xx: 
        401: Displayed if the email or password provided do not match a record in the Users table.
    """    
    body_data = request.get_json()
    query = db.select(User).filter_by(email=body_data.get("email"))
    user = db.session.scalar(query)
    if user and bcrypt.check_password_hash(user.password, body_data.get("password")):
        token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(days=1)
        )
        return {"email": user.email, "token": token}
    else:
        return {"error": "Invalid email or password"}, 401
