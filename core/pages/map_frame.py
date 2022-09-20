import time
import logging
from core.drivers import Driver
from selenium.webdriver.common.by import By
from commons.utils import log_data
import allure


class MapFrame:
    def __init__(self, driver: Driver, frame=None):
        self._driver = driver
        self._tab = 0
        self._frame = frame

    _locators = {"map": (By.XPATH, '//*[@id="mapDiv"]/div/div/div[4]/div/div/div/div'),
                 "map_change_look": (By.CLASS_NAME, 'gm-inset-map'),
                 "link": (By.XPATH, '//*[@id="mapDiv"]/div/div/div[4]/div/div/div/div/div[4]/div/a'),
                 "cordin": (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div['
                                      '1]/h2/span'),
                 "map_div": (By.ID, 'QA0Szd')}

    def get_map_details(self) -> str:
        map = self._driver.locate_element(self._locators["map"], self._frame)
        txt = self._driver.text(map)
        with allure.step(f"get map details = {txt}"):
            return txt

    def get_map_cordin_in_float(self):
        link = self._driver.locate_element(self._locators['link'], self._frame)
        link.click()

        if self._driver.type == "playwright":
            time.sleep(2)
            logging.info(self._driver.url)
            link.click()
            time.sleep(2)

        self._tab = self._driver.switch_to_tab(1)

        return self.parse_la_lo_from_gmaps(self._driver.url())

    def parse_la_lo_from_gmaps(self, val: str) -> tuple[float, float]:
        a = val.find("=")
        b = val.find("&")
        x = val[a + 1:b:]
        y = x.split(",")
        logging.info(self._driver.url)
        with allure.step(f"get map latitude, longtude = {x[0]},{y[1]}"):
            return float(y[0]), float(y[1])

    def change_look_style(self) -> str:
        btn = self._driver.locate_element(self._locators["map_change_look"], self._frame)
        txt = self._driver.get_attribute(btn, "title")
        btn.click()
        log_data(txt, msg="map style changed ->")
        with allure.step(f"change map look style = {txt}"):
            return txt

    def __del__(self):
        if self._tab != 0:
            self._driver.switch_to_tab(0)
