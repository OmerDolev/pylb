# imports
import requests
import vars
from pylb.targets.targets import *
import helpers
import flask
import multiprocessing
import os
app = flask.Flask(__name__)


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
    target = get_target()

    if target.is_empty():
        response = flask.Response(status="No healthy target found")
        response.status_code = 500
        return response

    proxy_pass_url = "http://{0}/{1}".format(get_target(), request.path)
    print(proxy_pass_url)
    try:
        response = requests.get(url=proxy_pass_url, headers=request.headers)
    except RuntimeError as e:
        terminate(vars.ec_runtime_error)
    finally:
        terminate(vars.ec_general_error)
    return response


def handle_post_request(request: flask.Request) -> flask.Response:
    return requests.post("")


def prepare_env(manager):
    vars.targets_pool = manager.list()
    populate_target_list_from_json(vars.targets_json_file)
    for t in Target.targetList:
        vars.targets_pool.append(t)
    vars.healthy_targets = manager.list()


def terminate(exit_code: int):
    print("{}\n".format(vars.errors_dict[exit_code]))
    exit(exit_code)


def get_target() -> Target:
    if not vars.healthy_targets:
        return Target.empty_target()

    selected_target = vars.healthy_targets[vars.rr_counter]
    vars.rr_counter = (vars.rr_counter+1) % len(vars.healthy_targets)
    return selected_target


if __name__ == '__main__':
    ipc_manager = multiprocessing.Manager()
    # start checking targets
    prepare_env(ipc_manager)
    p_target_health_check = multiprocessing.Process(target=helpers.update_healthy_targets_list)
    p_target_health_check.start()
    app.run(host='0.0.0.0', port=8090)
