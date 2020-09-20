from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy

from app.rest_utils import app_utils
from app.rest_utils.handlers import register_base_error_handlers

db = SQLAlchemy()


def create_app(env="production") -> Flask:
    app = Flask(__name__)
    app_utils.init_config(app, env, db_engines=["postgresql"])
    __init_db(app)
    __register_handlers(app)
    __init_security(app)

    app.config["BUNDLE_ERRORS"] = True

    return app


def __init_db(app: Flask):
    db.init_app(app)


def __init_security(app: Flask):
    from app.models import User

    user_datastore = SQLAlchemyUserDatastore(db, User, None)
    Security(app, user_datastore)


def __register_handlers(app: Flask):
    register_base_error_handlers(app)

