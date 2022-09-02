from common.driver import Driver

class Pdriver(Driver):
    def __init__(self, driver,type):
        super().__init__(driver,type)

    @staticmethod
    def By(by, locator):
        if by.value == "name":
            return f"[name={locator}]"

    def find_element(self, by, locator):
        locator = self.By(by, locator)
        return self.driver.locator(locator)