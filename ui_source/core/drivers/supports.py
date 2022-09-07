from ui_source.core.common.exceptions_ import *
from ui_source.core.common.constant import *
from ui_source.core.drivers.driver_p import PlayWright
from ui_source.core.drivers.driver_s import Selenium
from enum import Enum
from ui_source.core.drivers.driver import Driver

DRIVERS = {
    SELENIUM: Selenium,
    PLAYWRIGHT: PlayWright
}


class With(Enum):
    ID = "id"
    CLASS_NAME = "class name"
    NAME = "name"
    TAG_NAME = "tag name"
    XPATH = "xpath"
    CSS = "css selector"


def create_driver(lib, driver) -> Driver:
    if lib not in DRIVERS:
        raise LibNotSupport(f"lib must be {SELENIUM} or {PLAYWRIGHT} not {type(lib)}")
    return DRIVERS[lib](driver, lib)
