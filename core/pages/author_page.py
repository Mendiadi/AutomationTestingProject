import allure
from core.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from core.pages.map_frame import MapFrame
class AuthorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    _locators = {

        "map_frame": (By.ID, 'iframeId')

    }
    def out_map(self,map_:MapFrame):
        map_.__del__()
        if self._driver.type == "selenium":
            self._driver.switch_to_default()
        return self._driver.url

    def on_map(self):
        frame = self._driver.locate_element(self._locators["map_frame"])
        self._driver.locate_frame(frame)
        return MapFrame(self._driver)
