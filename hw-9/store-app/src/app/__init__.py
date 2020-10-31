from flask import Flask

from app.consumer import CONSUMERS
from app.db import db
from app.rest_utils import app_utils
from app.rest_utils.handlers import register_base_error_handlers
from app.threads import AppContextThread


def create_app(env="production") -> Flask:
    app = Flask(__name__)
    app_utils.init_config(app, env, db_engines=["postgresql"])
    __init_db(app)
    __register_handlers(app)
    __init_broker_handlers(app)

    app.config["BUNDLE_ERRORS"] = True

    return app


def __init_db(app: Flask):
    db.init_app(app)


def __register_handlers(app: Flask):
    register_base_error_handlers(app)


def __init_broker_handlers(app):
    app.app_context().push()
    for task in CONSUMERS:
        AppContextThread(target=task).start()
