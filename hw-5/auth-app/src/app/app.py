import os

from app import create_app
from app.rest_utils.view import json_response

app = create_app(env=os.environ.get("ENV"))


@app.route("/")
def home():
    return json_response(data={'hostname': app.config['HOSTNAME']})


if __name__ == "__main__":
    app.run(debug=True)
