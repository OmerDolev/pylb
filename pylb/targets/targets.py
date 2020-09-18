import multiprocessing
import json


class Target:
    targetList = []

    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port
        Target.targetList.append(self)

    def __str__(self):
        return "{0}:{1}".format(self.host, self.port)


# format of json file is expected to be as in ./data/init_targets.json
def populate_target_list_from_json(path: str):
    with open(path, "r") as f:
        json_data = json.load(f)
        for target in json_data["targets"]:
            curr_host = target.split(":")[0]
            curr_port = target.split(":")[1]
            Target(curr_host, curr_port)
