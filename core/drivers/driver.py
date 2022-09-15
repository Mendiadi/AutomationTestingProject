from __future__ import annotations
from abc import ABC, abstractmethod
from commons import LibNotSupport
from commons.constant import *
from playwright.sync_api import Page


class Driver(ABC):

    def __init__(self, driver, type_):
        self._driver = driver
        self._type = type_

    @staticmethod
    def create_driver(lib, driver) -> Driver:
        from core.drivers.driver_p import PlayWright
        from core.drivers.driver_s import Selenium
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
    def get_attribute(self, element, name: str) -> [str]:
        pass

    @abstractmethod
    def switch_to_tab(self,val:int):
        pass

    def url(self):
        pass

    @abstractmethod
    def script_execute(self, __script: str):
        pass

    @abstractmethod
    def get_screenshot(self) -> bytes:
        pass
    def switch_to_default(self):
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
            try:
                return locator.text_content()
            except:
                return
        elif self._type == SELENIUM:
            return locator.text

    def alert_text(self, alert_var) -> str:
        pass

    def move_to_element(self, element):
        pass

    def switch_to_alert(self, input__=""):
        pass

    def alert_accepted(self, alert_var):
        pass

    def refresh(self):
        if self._type.lower() == PLAYWRIGHT:
            self._driver.reload()
        else:
            self._driver.refresh()
