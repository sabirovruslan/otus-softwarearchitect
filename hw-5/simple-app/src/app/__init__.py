from flask import Flask

from app.rest_utils import app_utils
from app.rest_utils.handlers import register_base_error_handlers


def create_app(env="production") -> Flask:
    app = Flask(__name__)
    app_utils.init_config(app, env)
    __register_handlers(app)

    app.config["BUNDLE_ERRORS"] = True

    return app


def __register_handlers(app: Flask):
    register_base_error_handlers(app)
