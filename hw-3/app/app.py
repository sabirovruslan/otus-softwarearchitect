import json
import os

from flask import Flask, Response
from metrics import register_metrics
from prometheus_client import generate_latest
from sqlalchemy import create_engine
from webargs import fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ['HOSTNAME'],
}


@app.route("/")
def hello():
    return json_response(data={'hostname': config['HOSTNAME']})


@app.route('/users/add', methods=['POST'])
@use_kwargs({
    'name': fields.String(required=True),
    'surname': fields.String(required=True),
    'login': fields.String(required=True),
}, location="form")
def add_user(name: str, surname: str, login: str):
    with db().connect() as connection:
        with connection.begin():
            connection.execute(
                f"insert into users (name, surname, login) values ('{name}', '{surname}', '{login}');"
            )
        result = connection.execute(f"select id from users where login='{login}';")
        rows = [dict(r.items()) for r in result]
    return json_response(data=rows[0] if len(rows) > 0 else None)


@app.route('/users/<int:uid>', methods=['PUT'])
@use_kwargs({
    'name': fields.String(required=True),
    'surname': fields.String(required=True),
}, location="form")
def update_user(name: str, surname: str, uid: int):
    with db().connect() as connection:
        with connection.begin():
            connection.execute(
                f"update users set name = '{name}', surname = '{surname}' WHERE id = {uid};"
            )
    return json_response()


@app.route('/users/<int:uid>', methods=['DELETE'])
def delete_user(uid: int):
    with db().connect() as connection:
        with connection.begin():
            connection.execute(
                f"delete from users WHERE id = {uid};"
            )
    return json_response()


@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid: int):
    with db().connect() as connection:
        result = connection.execute(f"select id, name, surname, login from users where id = {uid};")
        rows = [dict(r.items()) for r in result]
    return json_response(data=rows[0] if len(rows) > 0 else None)


@app.route('/users', methods=['GET'])
def get_users():
    with db().connect() as connection:
        result = connection.execute("select id, name, surname, login from users;")
        rows = [dict(r.items()) for r in result]
    return json_response(data=rows)


@app.route('/metrics')
def metrics():
    return generate_latest()


@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    return Response(
        json.dumps({"errors": err.data.get("messages", ["Invalid request."])}),
        status=err.code,
        headers=err.data.get("headers", None),
        mimetype="application/json",
    )


def json_response(data=None, status_code=200, headers=None):
    return Response(
        json.dumps({"data": data}),
        status=status_code,
        headers=headers,
        mimetype="application/json",
    )


def db():
    return create_engine(config['DATABASE_URI'], echo=True)


if __name__ == "__main__":
    register_metrics(app)
    app.run(host='0.0.0.0', port='80', debug=True)
