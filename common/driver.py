
from common.constant import *
from abc import ABC





class Driver(ABC):

    def __init__(self, driver, type):
        self.driver = driver
        self._type = type

    @property
    def type(self) -> str:
        return self._type

    def send_keys(self, locator, input):
        if self._type == PLAYWRIGHT:
            locator.fill(input)
        elif self._type == SELENIUM:
            locator.send_keys(input)









