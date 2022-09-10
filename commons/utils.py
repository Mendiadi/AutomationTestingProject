import json


def json_read(path) -> json:
    try:
        with open(path, "r") as json_file:
            json_file = json.load(json_file)

    except FileNotFoundError:
        with open(rf"tests\{path}", "r") as json_file:
            json_file = json.load(json_file)
    finally:
        return json_file


import yaml


def parse_yaml():
    with open("./api_manage.yaml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
