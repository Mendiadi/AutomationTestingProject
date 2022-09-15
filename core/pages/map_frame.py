from core.drivers import Driver
from selenium.webdriver.common.by import By
import keyboard
import allure
class MapFrame:
    def __init__(self,driver:Driver):
        self._driver = driver
        self._tab = 0

    _locators = {"map": (By.XPATH, '//*[@id="mapDiv"]/div/div/div[4]/div/div/div/div'),

        "map_change_look":(By.CLASS_NAME,'gm-inset-map'),"link":(By.XPATH,'//*[@id="mapDiv"]/div/div/div[4]/div/div/div/div/div[4]/div/a')
                 ,"cordin":(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/h2/span'),
                 "map_div":(By.ID,'QA0Szd')}



    def get_map_details(self):
        map = self._driver.locate_element(self._locators["map"])
        txt = self._driver.text(map)
        with allure.step(f"get map details = {txt}"):
            return txt

    def get_map_cordin_in_float(self):
        link = self._driver.locate_element(self._locators['link'])
        link.click()
        self._tab = self._driver.switch_to_tab(1)

        return self._convert_cordinates(self._driver.url)

    def _convert_cordinates(self,val:str) -> tuple[float,float]:
        a =val.find("=")
        b = val.find("&")
        x = val[a+1:b:]
        y = x.split(",")
        with allure.step(f"get map latitude, longtude = {x[0]},{y[1]}"):
            return (float(y[0]),float(y[1]))


    def change_look_style(self) -> str:
        btn = self._driver.locate_element(self._locators["map_change_look"])
        txt = self._driver.get_attribute(btn,"title")
        btn.click()
        with allure.step(f"change map look style = {txt}"):
            return txt

    def scroll_left(self):
        keyboard.press("left")
        keyboard.release("left")


    def __del__(self):
        if self._tab != 0:
            self._driver.switch_to_tab(0)

