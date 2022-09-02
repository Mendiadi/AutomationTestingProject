class BasePage:
    def __init__(self, driver):
        self._driver = driver

    @property
    def title(self) -> str:
        pass
