# imports
import requests
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def handle_get_request(request: requests.Request) -> requests.Response:
    return requests.get("")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)

