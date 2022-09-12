from __future__ import annotations
from ui_source.core.constant import *
from abc import ABC, abstractmethod
from ui_source.core.exceptions_ import LibNotSupport


class Driver(ABC):

    def __init__(self, driver, type_):
        self._driver = driver
        self._type = type_

    @staticmethod
    def create_driver(lib, driver) -> Driver:
        from ui_source.core.drivers.driver_p import PlayWright
        from ui_source.core.drivers.driver_s import Selenium
        DRIVERS = {
            SELENIUM: Selenium,
            PLAYWRIGHT: PlayWright}
        if lib not in DRIVERS:
            raise LibNotSupport(f"lib must be {SELENIUM} or {PLAYWRIGHT} not {type(lib)}")
        return DRIVERS[lib](driver, lib)

    @abstractmethod
    def locate_element(self, locator: tuple[[], str], driver: [] = None) -> []:
        pass

    @abstractmethod
    def locate_elements(self, locator: tuple[[], str]) -> []:
        pass

    @abstractmethod
    def locate_frame(self, locator: tuple[[], str]) -> []:
        pass

    @abstractmethod
    def script_execute(self, __script: str):
        pass

    @abstractmethod
    def get_screenshot(self) -> bytes:
        pass

    @property
    def title(self) -> str:
        if self._type == SELENIUM:
            return self._driver.title
        elif self._type == PLAYWRIGHT:
            return self._driver.title()

    def element_is_visible(self, locator) -> bool:
        pass
    @property
    def type(self) -> str:
        return self._type

    def send_keys(self, locator, input_):
        if self._type == PLAYWRIGHT:
            locator.fill(input_)
        elif self._type == SELENIUM:
            locator.send_keys(input_)

    def text(self, locator) -> str:
        """
        getting text of locator
        :param locator: element/locator
        :return: string of text content
        """
        if self._type == PLAYWRIGHT:
            return locator.text_content()
        elif self._type == SELENIUM:
            return locator.text

    def alert_text(self, alert_var) -> str:
        pass

    def switch_to_alert(self, input__=""):
        pass
    def alert_accepted(self,alert_var):
        pass