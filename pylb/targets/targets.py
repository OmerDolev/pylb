import json


class Target:
    targetList = []

    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port
        Target.targetList.append(self)

    def __str__(self):
        return "{0}:{1}".format(self.host, self.port)

    def is_empty(self):
        if self.host == "" and self.port == "":
            return True
        return False

    def is_in_list(self, t_list):
        for t in t_list:
            if is_equal(self, t):
                return True
        return False

    @staticmethod
    def empty_target():
        return Target("", "")


# check if two targets are equal
def is_equal(first: Target, second: Target):
    return True if first.host == second.host and first.port == second.port else False


# format of json file is expected to be as in ./data/init_targets.json
def populate_target_list_from_json(path: str):
    with open(path, "r") as f:
        json_data = json.load(f)
        for target in json_data["targets"]:
            curr_host = target.split(":")[0]
            curr_port = target.split(":")[1]
            Target(curr_host, curr_port)
