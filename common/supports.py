from common.exceptions_test import *
from common.constant import *
from common.driver_p import Pdriver
from common.driver_s import Sdriver
from enum import Enum
from common.driver import Driver

DRIVERS = {
    SELENIUM: Sdriver,
    PLAYWRIGHT: Pdriver
}


class With(Enum):
    ID = "id"
    CLASS_NAME = "class_name"
    NAME = "name"
    TAG_NAME = "tag_name"
    XPATH = "xpath"
    CSS = "css"


def create_driver(lib, driver) -> Driver:
    if lib not in DRIVERS:
        raise LibNotSupport(f"lib must be {SELENIUM} or {PLAYWRIGHT} not {type(lib)}")
    return DRIVERS[lib](driver, lib)
