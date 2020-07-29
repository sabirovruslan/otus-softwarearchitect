import os
import time

from flask import Flask

app = Flask(__name__)


@app.route("/health")
def health():
    return '{"status": "ok"}'


@app.route("/version")
def version():
    return '{"version": "0.1"}'


@app.route("/")
def hello():
    return 'Hello world from v2 ' + os.environ['HOSTNAME'] + ' !'


if __name__ == "__main__":
    time.sleep(7)
    app.run(host='0.0.0.0', port='80')
