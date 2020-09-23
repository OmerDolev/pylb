from os.path import dirname as up
import os
import sys

# this is a general var list
targets_pool = []
healthy_targets = []
rr_counter = 0
health_check_interval_seconds = 1

if sys.executable.endswith("exe"):
    targets_json_file = '{0}\data\init_targets.json'.format(up(up(os.path.realpath(__file__))))
else:
    targets_json_file = '{0}/data/init_targets.json'.format(up(up(os.path.realpath(__file__))))

# error and exception handling
ec_success = 0
ec_runtime_error = 1
ec_general_error = 2
ec_keyboard_int = 3

errors_dict = {
    ec_success: "execution finished successfully!",
    ec_runtime_error: "runtime exception occured, exiting...",
    ec_general_error: "general error occured, exiting..."
}
