import json
import allure
import yaml
import os


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


def write_to_json(data: dict,path):
    json_object = json.dumps(data, indent=3)
    with open(path, "w") as outfile:
        outfile.write(json_object)


def screenshot_if_failed(driver, request):
    if request.node.rep_call.failed:
        try:
            driver.script_execute("document.body.bgColor = 'white';")
            allure.attach(driver.get_screenshot(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)
        except:

            pass
