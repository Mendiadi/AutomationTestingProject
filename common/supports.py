from common.exceptions_test import *
from common.constant import *
from common.driver_p import Pdriver
from common.driver_s import Sdriver
from enum import Enum


class With(Enum):
    ID = "id"
    CLASS_NAME = "class_name"
    NAME = "name"
    TAG_NAME = "tag_name"
    XPATH = "xpath"
    CSS = "css"


def create_driver(lib, driver):
    if lib == PLAYWRIGHT:
        return Pdriver(driver, PLAYWRIGHT)
    elif lib == SELENIUM:
        return Sdriver(driver, SELENIUM)
    else:
        raise LibNotSupport(f"lib must be {SELENIUM} or {PLAYWRIGHT} not {type(lib)}")
