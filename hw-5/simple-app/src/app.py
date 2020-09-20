import json
import os

from flask import Flask, Response

app = Flask(__name__)

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ['HOSTNAME'],
}


@app.route("/")
def hello():
    return json_response(data={'hostname': config['HOSTNAME']})


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
