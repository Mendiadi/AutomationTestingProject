from UI.common.driver import Driver


class BasePage:
    def __init__(self, driver: Driver):
        self._driver = driver

    @property
    def title(self) -> str:
        return self._driver.title
