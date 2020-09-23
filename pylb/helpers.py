import socket
from targets.targets import *
import flask
import requests


def is_port_open(target: Target):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex((target.host, int(target.port)))
        if result == 0:
            return True
        return False
