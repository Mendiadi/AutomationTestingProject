import json

def json_read(path) -> json:
    with open(path,"r") as f:
        obj = json.load(f)
    return obj