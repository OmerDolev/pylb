# this is a general var list
targets_pool = []
healthy_targets = []
targets_json_file = "../data/init_targets.json"

# error and exception handling
ec_success = 0
ec_runtime_error = 1
ec_general_error = 2

errors_dict = {
    ec_success: "execution finished successfully!",
    ec_runtime_error: "runtime exception occured, exiting...",
    ec_general_error: "general error occured, exiting..."
}
