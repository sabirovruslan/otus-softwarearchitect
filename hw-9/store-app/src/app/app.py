import os

from webargs import fields
from webargs.flaskparser import use_kwargs

from app import create_app
from app.response_schema import health_schema
from app.rest_utils.view import json_response
from app.stories import GetOrderStoreStory

app = create_app(env=os.environ.get('ENV'))


@app.route('/v1/store/', methods=['GET'])
@use_kwargs({
    'order_id': fields.Integer(required=True),
}, location='query')
def get_store(order_id: int):
    return json_response(data=GetOrderStoreStory().execute(order_id))


@app.route('/health')
def health():
    return json_response(data=health_schema())


if __name__ == '__main__':
    app.run(debug=True)
