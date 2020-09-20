import os

from webargs import fields
from webargs import validate
from webargs.flaskparser import use_kwargs

from app import create_app
from app.exceptions import StoreValidation
from app.rest_utils.exceptions import BadRequest
from app.rest_utils.view import json_response
from app.stories import UserStoreStory, GetConfirmationStory

app = create_app(env=os.environ.get("ENV"))


@app.route("/")
def home():
    return json_response(data={'hostname': app.config['HOSTNAME']})


@app.route("/users", methods=['POST'])
@use_kwargs({
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'phone': fields.Int(required=True, validate=validate.Range(10000000000, 79999999999)),
}, location="form")
def register_user(**kwargs):
    try:
        return json_response(data=UserStoreStory().execute(**kwargs))
    except StoreValidation as e:
        raise BadRequest(message=str(e))


@app.route("/users/confirmation", methods=['GET'])
@use_kwargs({
    'phone': fields.Int(required=True, validate=validate.Range(10000000000, 79999999999)),
}, location="query")
def get_confirmation(phone: int):
    try:
        GetConfirmationStory().execute(phone)
        return json_response()
    except StoreValidation as e:
        raise BadRequest(message=str(e))


if __name__ == "__main__":
    app.run(debug=True)
