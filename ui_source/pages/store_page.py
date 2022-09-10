from ui_source.pages.base_page import BasePage
from selenium.webdriver.common.by import By

class StorePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)


    _locators = {

        "h1_label":(By.TAG_NAME,'h1')
    }

    def get_label_h1_text(self) -> str:

        label = self._driver.locate_element(self._locators["h1_label"])
        return self._driver.text(label)