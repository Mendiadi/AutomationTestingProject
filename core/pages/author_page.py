import allure
from core.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class AuthorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    _locators = {

        "map": (By.XPATH, '//*[@id="mapDiv"]/div/div/div[4]/div/div/div/div'),
        "map_frame":(By.ID,'iframeId')

    }

    def get_map_cordinate(self):
        frame = self._driver.locate_element(self._locators["map_frame"])
        self._driver.locate_frame(frame)
        map = self._driver.locate_element(self._locators["map"])
        txt = self._driver.text(map)
        if self._driver.type == "selenium":
            self._driver.switch_to_default()
        return txt