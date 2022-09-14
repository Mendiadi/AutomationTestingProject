from core.drivers import Driver
from selenium.webdriver.common.by import By
import keyboard
class MapFrame:
    def __init__(self,driver:Driver):
        self._driver = driver


    _locators = {"map": (By.XPATH, '//*[@id="mapDiv"]/div/div/div[4]/div/div/div/div'),

        "map_change_look":(By.CLASS_NAME,'gm-inset-map')}



    def get_map_cordinate(self):
        map = self._driver.locate_element(self._locators["map"])
        txt = self._driver.text(map)
        return txt




    def change_look_style(self) -> str:
        btn = self._driver.locate_element(self._locators["map_change_look"])
        txt = self._driver.text(btn)
        btn.click()
        return txt

    def scroll_left(self):
        keyboard.press("left")
        keyboard.release("left")