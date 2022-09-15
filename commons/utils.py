import json
import yaml


def json_read(path) -> json:
    try:
        with open(path, "r") as json_file:
            json_file = json.load(json_file)

    except FileNotFoundError:
        with open(rf"tests\{path}", "r") as json_file:
            json_file = json.load(json_file)
    finally:
        return json_file


def parse_yaml():
    with open("./api_manage.yaml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def write_to_json(data: dict, path):
    json_object = json.dumps(data, indent=1)
    with open(path, "w") as outfile:
        outfile.write(json_object)

