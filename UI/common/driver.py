from UI.common.constant import *
from abc import ABC, abstractmethod


class Driver(ABC):

    def __init__(self, driver, type_):
        self._driver = driver
        self._type = type_

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

