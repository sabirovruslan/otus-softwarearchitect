from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.rest_utils import app_utils
from app.rest_utils.handlers import register_base_error_handlers

db = SQLAlchemy()


def create_app(env="production") -> Flask:
    app = Flask(__name__)
    app_utils.init_config(app, env, db_engines=["postgresql"])
    __init_db(app)
    __register_handlers(app)

    app.config["BUNDLE_ERRORS"] = True

    return app


def __init_db(app: Flask):
    db.init_app(app)


def __register_handlers(app: Flask):
    register_base_error_handlers(app)



# from app import models  # noqa F401
