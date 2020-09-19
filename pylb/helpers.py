import socket
from pylb.targets.targets import *
import vars
import time

def is_port_open(target: Target):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((target.host, target.port))
        if result == 0:
            return True
        return False


def update_healthy_targets_list():
    print(vars.targets_pool)
    while True:
        for target in vars.targets_pool:
            print("checking {}".format(target))
            is_open = is_port_open(target)
            if is_open and target not in vars.healthy_targets:
                vars.healthy_targets.append(target)
            elif not is_open and target in vars.healthy_targets:
                vars.healthy_targets.remove(target)
        print(vars.healthy_targets)
        time.sleep(vars.health_check_interval_seconds)
