from common.driver import Driver
from selenium.webdriver.common.by import By


class Sdriver(Driver):
    def __init__(self, driver,type):
        super().__init__(driver,type)

    @staticmethod
    def By(by, locator):
        if by.value == "name":
            return (By.NAME, locator)

    def find_element(self, by, locator):
        locator = self.By(by, locator)
        return self.driver.find_element(*locator)