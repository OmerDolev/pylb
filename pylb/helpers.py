import socket
from pylb.targets.targets import *


def is_port_open(target: Target):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((target.host, target.port))
        if result == 0:
            return True
        return False

