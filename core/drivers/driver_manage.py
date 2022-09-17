from playwright.sync_api import sync_playwright
from selenium import webdriver
import ctypes
from commons.constant import *
from core.drivers import Driver
from commons import LibNotSupport


class DriverContextManager:

    def __init__(self,configuration):
        self._page = None
        self._config = configuration


    def init(self) -> Driver:
        from core.drivers.driver_p import PlayWright
        from core.drivers.driver_s import Selenium
        DRIVERS = {
            SELENIUM: Selenium,
            PLAYWRIGHT: PlayWright}
        if self._config.lib not in DRIVERS:
            raise LibNotSupport(f"lib must be {SELENIUM} or {PLAYWRIGHT} not {type(self._config.lib)}")
        return DRIVERS[self._config.lib](self._page, self._config.lib)

    def _on_playwright(self):
        user32 = ctypes.windll.user32
        p = sync_playwright().start()
        if self._config.browser == CHROME:
            driver = p.chromium.launch(headless=False)
        else:
            driver = p.firefox.launch(headless=False)
        self._page = driver.new_page()
        self._page.goto(self._config.url)
        screensize = {"width": user32.GetSystemMetrics(0), "height": user32.GetSystemMetrics(1)}
        self._page.set_viewport_size(viewport_size=screensize)


    def _on_selenium_grid(self):
        if self._config.browser == CHROME:
            chrome_options = webdriver.ChromeOptions()
            capabilities = webdriver.DesiredCapabilities.CHROME
        elif self._config.browser == FIREFOX:
            chrome_options = webdriver.FirefoxOptions()
            capabilities = webdriver.DesiredCapabilities.FIREFOX
        self._page = webdriver.Remote(
            command_executor=f"http://localhost:4444/wd/hub",
            options=chrome_options,
            desired_capabilities=capabilities
        )

    def _on_selenium(self):
        if self._config.selenium_grid:
            self._on_selenium_grid()
        else:
            if self._config.browser == CHROME:
                self._page = webdriver.Chrome(self._config.driver_path)
            elif self._config.browser == FIREFOX:
                self._page = webdriver.Firefox(self._config.driver_path)
        self._page.get(self._config.url)
        self._page.maximize_window()


    def __enter__(self):
        if self._config.lib == PLAYWRIGHT:
            self._on_playwright()
        elif self._config.lib == SELENIUM:
            self._on_selenium()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._page.close()