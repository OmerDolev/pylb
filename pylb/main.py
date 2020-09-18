# imports
import requests
from .vars import *
from pylb.targets.targets import *
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def handle_get_request(request: requests.Request) -> requests.Response:
    return requests.get("")


def handle_post_request(request: requests.Request) -> requests.Response:
    return requests.post("")


def prepare_env():
    targets_pool = populate_target_list_from_json(targets_json_file)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
