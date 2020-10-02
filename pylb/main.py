# imports
import time
import requests
import vars
import targets.targets as t
import helpers
import flask
import multiprocessing
app = flask.Flask(__name__)


@app.route('/')
@app.route('/<path>', methods=['GET', 'POST'])
def main(path="nopath"):
    # TODO: handle multiple paths
    target = get_target()

    if target.is_empty():
        response = flask.Response(response="No healthy target found")
        response.status_code = 500
        return response

    if flask.request.method == "GET":
        response = handle_get_request(flask.request, target)
    else:
        response = handle_post_request(flask.request, target)

    return response


def handle_get_request(request: flask.Request, target: t.Target):
    # format target url
    proxy_pass_url = "http://{0}{1}".format(target, request.path)

    try:
        r_response = requests.get(url=proxy_pass_url, headers=request.headers)
    except RuntimeError as e:
        terminate(vars.ec_runtime_error)
    return r_response.text, r_response.status_code


def handle_post_request(request: flask.Request, target: t.Target) -> flask.Response:
    # format target url
    proxy_pass_url = "http://{0}{1}".format(target, request.path)

    try:
        r_response = requests.post(url=proxy_pass_url, headers=request.headers)
    except RuntimeError as e:
        terminate(vars.ec_runtime_error)
    return r_response.text, r_response.status_code


@app.route('/targets')
def path_targets():
    output = "\n"
    for idx, current_target in enumerate(healthy_targets):
        output += "Target {}: {}\n".format(idx, current_target)
    output += "\n"

    response = flask.Response(response=output)
    response.status_code = 200
    return response


def terminate(exit_code: int):
    print("{}\n".format(vars.errors_dict[exit_code]))
    exit(exit_code)


# round-robin targets for requests
def get_target() -> t.Target:
    global rr_counter
    if not healthy_targets:
        return t.Target.empty_target()

    selected_target = healthy_targets[rr_counter]
    rr_counter = (rr_counter+1) % len(healthy_targets)
    return selected_target


def update_healthy_targets_list(t_pool, h_targets):
    while True:
        for target in t_pool:
            # check if port is open
            # and if target is in healthy targets list
            is_open = helpers.is_port_open(target)
            if is_open and not target.is_in_list(h_targets):
                h_targets.append(target)
            elif not is_open and target.is_in_list(h_targets):
                h_targets.remove(target)

        time.sleep(vars.health_check_interval_seconds)


if __name__ == '__main__':

    # muttable variables in global scope
    ipc_manager = multiprocessing.Manager()
    targets_pool = ipc_manager.list()
    healthy_targets = ipc_manager.list()
    rr_counter = 0

    t.populate_target_list_from_json(vars.targets_json_file)
    for tgt in t.Target.targetList:
        targets_pool.append(tgt)

    # start checking targets health
    p_target_health_check = multiprocessing.Process(target=update_healthy_targets_list,
                                                    args=(targets_pool, healthy_targets))
    p_target_health_check.start()

    app.run(host='0.0.0.0', port=8090)
