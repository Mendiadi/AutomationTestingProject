from pages.base_page import BasePage
from common.supports import With


class MainPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    _locators = {
        "search_bar": (With.NAME, "q")
    }

    def search(self, keys):
        search = self._driver.locate_element(self._locators['search_bar'])
        self._driver.send_keys(search, keys)
