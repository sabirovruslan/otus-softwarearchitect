import os

from webargs import fields
from webargs.flaskparser import use_kwargs

from app import create_app
from app.auth_context import auth_context, AuthContext
from app.exceptions import StoreValidation
from app.response_schema import health_schema
from app.rest_utils.exceptions import BadRequest
from app.rest_utils.view import json_response
from app.stories import GetOrdersStory, OrderStoreStory

app = create_app(env=os.environ.get('ENV'))


@app.route('/')
def home():
    return json_response(data={'hostname': app.config['HOSTNAME']})


@app.route('/v1/orders/', methods=['GET'])
@auth_context()
def get_orders(ctx: AuthContext):
    return json_response(data=GetOrdersStory().execute(ctx))


@app.route('/v1/orders/', methods=['POST'])
@use_kwargs({
    'total_price': fields.String(required=True),
    'if_match': fields.Int(required=True),
}, location='form')
@auth_context()
def create_order(total_price, ctx: AuthContext, if_match: int):
    try:
        return json_response(data=OrderStoreStory().execute(total_price, ctx, if_match))
    except StoreValidation as e:
        raise BadRequest(message=str(e))


@app.route('/health')
def health():
    return json_response(data=health_schema())


if __name__ == '__main__':
    app.run(debug=True)
