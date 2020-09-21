import os

from app import create_app
from app.auth_context import AuthContext, auth_context
from app.response_schema import health_schema, ctx_profile_schema
from app.rest_utils.view import json_response

app = create_app(env=os.environ.get('ENV'))


@app.route('/')
def home():
    return json_response(data={'hostname': app.config['HOSTNAME']})


@app.route('/users/profile', methods=['GET'])
@auth_context()
def update(ctx: AuthContext):
    return json_response(data=ctx_profile_schema(ctx))


@app.route('/health')
def health():
    return json_response(data=health_schema())


if __name__ == '__main__':
    app.run(debug=True)
