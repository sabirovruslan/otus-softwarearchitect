import os

from webargs import fields
from webargs.flaskparser import use_kwargs

from app import create_app
from app.exceptions import StoreValidation
from app.response_schema import health_schema
from app.rest_utils.exceptions import BadRequest
from app.rest_utils.view import json_response

app = create_app(env=os.environ.get('ENV'))


@app.route('/')
def home():
    return json_response(data={'hostname': app.config['HOSTNAME']})


@app.route('/v1/orders/', methods=['POST'])
@use_kwargs({
    'order_price': fields.Int(required=True),
}, location='form')
def register(**kwargs):
    try:
        return json_response(data=OrderStoreStory().execute(**kwargs))
    except StoreValidation as e:
        raise BadRequest(message=str(e))


@app.route('/health')
def health():
    return json_response(data=health_schema())


if __name__ == '__main__':
    app.run(debug=True)
