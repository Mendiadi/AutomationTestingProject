from __future__ import annotations
from abc import ABCMeta, abstractmethod

from commons.constant import *


class Driver(metaclass=ABCMeta):

    def __init__(self, driver, type_):
        self._driver = driver
        self._type = type_

    @abstractmethod
    def locate_element(
            self,
            locator: tuple[[], str],
            driver: [] = None
    ) -> []:
        ...

    @abstractmethod
    def locate_elements(
            self,
            locator: tuple[..., str]
    ) -> []:
        ...

    @abstractmethod
    def locate_frame(
            self,
            locator: tuple[[], str]
    ) -> []:
        ...

    @abstractmethod
    def get_attribute(
            self,
            element,
            name: str
    ) -> [str]:
        ...

    @abstractmethod
    def switch_to_tab(
            self,
            val: int
    ):
        ...

    def url(self) -> str:
        ...

    @abstractmethod
    def script_execute(self, __script: str):
        ...

    @abstractmethod
    def get_screenshot(self) -> bytes:
        ...

    def switch_to_default(self):
        ...

    @property
    def title(self) -> str:
        if self._type == SELENIUM:
            return self._driver.title
        elif self._type == PLAYWRIGHT:
            return self._driver.title()

    def element_is_visible(self, locator) -> bool:
        ...

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
                pass
        elif self._type == SELENIUM:
            return locator.text

    def alert_text(self, alert_var) -> str:
        ...

    def move_to_element(self, element):
        ...

    def switch_to_alert(self, input__=""):
        ...

    def alert_accepted(self, alert_var):
        ...

    def refresh(self):
        if self._type.lower() == PLAYWRIGHT:
            self._driver.reload()
        else:
            self._driver.refresh()
