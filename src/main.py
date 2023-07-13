from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    # creating the Flask app:
    app = Flask(__name__)

    # importing app configuration from config.py:
    app.config.from_object("config.app_config")

    # initialising the app:
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # importing and activating CLI commands:
    from controllers.commands_controller import db_commands

    app.register_blueprint(db_commands)

    # importing and activating controllers and blueprints:
    from controllers import controllers

    for controller in controllers:
        app.register_blueprint(controller)

    return app
