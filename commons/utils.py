import json
import os
import yaml
import logging
import functools
from typing import Callable


def json_read(path: str) -> json:
    try:
        with open(path, "r") as json_file:
            json_file = json.load(json_file)

    except FileNotFoundError:
        with open(rf"tests\{path}", "r") as json_file:
            json_file = json.load(json_file)
    finally:
        return json_file


def parse_yaml(path: str) -> None:
    with open(path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def write_to_json(data: dict, path: str, indent: int = 1) -> None:
    json_object = json.dumps(data, indent=indent)
    with open(os.path.abspath(path), "w") as outfile:
        outfile.write(json_object)


logger = logging.getLogger(__name__)


def log_data(*args: [...], msg: str = "") -> None:
    try:
        logger.info(f"""
       {msg} -> {" | ".join(args)}
    """)
    except TypeError:
        logger.info(f"""
               {msg} -> {args}
            """)


def log_name(func: Callable) -> Callable[..., None]:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}\n")
        func(*args, **kwargs)

    return wrapper
