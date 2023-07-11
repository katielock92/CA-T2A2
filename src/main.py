from flask import Flask
from init import db, ma, bcrypt, jwt
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.app_config")

    # add error handling here

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # register blueprints here

    return app
