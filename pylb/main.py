# imports
import requests
from .vars import *
from pylb.targets.targets import *
import flask
import multiprocessing
app = flask.Flask(__name__)
ipc_manager = multiprocessing.Manager()


@app.route('/')
def main():

    if flask.request.method == "GET":
        response = handle_get_request(flask.request)
    elif flask.request.method == "POST":
        response = handle_post_request(flask.request)
    else:
        response = flask.Response(status="LB does not support the request method")
        response.status_code = 400

    return response


def handle_get_request(request: flask.Request) -> flask.Response:
    try:
        response = requests.get(url=request.url, headers=request.headers)
    except RuntimeError as e:
        terminate(ec_runtime_error)
    finally:
        terminate(ec_general_error)
    return


def handle_post_request(request: flask.Request) -> flask.Response:
    return requests.post("")


def prepare_env():
    targets_pool = populate_target_list_from_json(targets_json_file)
    healthy_targets = ipc_manager.list()


def terminate(exit_code: int):
    print("{}\n".format(errors_dict[exit_code]))
    exit(exit_code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
