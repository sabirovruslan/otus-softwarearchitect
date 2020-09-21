import os

from webargs import fields
from webargs import validate
from webargs.flaskparser import use_kwargs

from app import create_app
from app.auth_context import AuthContext, auth_context
from app.exceptions import StoreValidation
from app.response_schema import health_schema, jwks_schema
from app.rest_utils.exceptions import BadRequest
from app.rest_utils.view import json_response
from app.stories import UserStoreStory, GetConfirmationStory, UserLoginStory, UserUpdateByCtxStory

app = create_app(env=os.environ.get('ENV'))


@app.route('/')
def home():
    return json_response(data={'hostname': app.config['HOSTNAME']})


@app.route('/users', methods=['POST'])
@use_kwargs({
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'phone': fields.Int(required=True, validate=validate.Range(10000000000, 79999999999)),
}, location='form')
def register(**kwargs):
    try:
        return json_response(data=UserStoreStory().execute(**kwargs))
    except StoreValidation as e:
        raise BadRequest(message=str(e))


@app.route('/users/confirmation', methods=['GET'])
@use_kwargs({
    'phone': fields.Int(required=True, validate=validate.Range(10000000000, 79999999999)),
}, location='query')
def get_confirmation(phone: int):
    try:
        GetConfirmationStory().execute(phone)
        return json_response()
    except StoreValidation as e:
        raise BadRequest(message=str(e))


@app.route('/users/login', methods=['POST'])
@use_kwargs({
    'phone': fields.Int(required=True, validate=validate.Range(10000000000, 79999999999)),
    'pin': fields.Int(required=True, validate=validate.Range(10000, 99999)),
}, location='form')
def login(phone: int, pin: int):
    try:
        return json_response(UserLoginStory().execute(phone, pin))
    except StoreValidation as e:
        raise BadRequest(message=str(e))


@app.route('/users', methods=['PUT'])
@use_kwargs({
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
}, location='form')
@auth_context()
def update(ctx: AuthContext, first_name, last_name):
    try:
        return json_response(data=UserUpdateByCtxStory().execute(ctx, first_name, last_name))
    except StoreValidation as e:
        raise BadRequest(message=str(e))


@app.route('/.well-known/jwks.json')
def jwks():
    return jwks_schema()


@app.route('/health')
def health():
    return json_response(data=health_schema())


if __name__ == '__main__':
    app.run(debug=True)
