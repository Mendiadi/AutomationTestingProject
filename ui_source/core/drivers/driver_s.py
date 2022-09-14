import time

from ui_source.core.drivers.driver import Driver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class Selenium(Driver):
    def __init__(self, driver, type_):
        self.wait = 5
        super().__init__(driver, type_)

    def switch_to_alert(self, input__=""):
        alert_var = self._driver.switch_to.alert
        t = alert_var.text
        alert_var.accept()
        return t

    def move_to_element(self,element):
        actions = ActionChains(self._driver)
        actions.scroll_to_element(element)
        elem = actions.move_to_element(element)
        time.sleep(0.5)
        elem.click().perform()


    def element_is_visible(self, locator) -> [bool]:
        try:
            result = WebDriverWait(self._driver, self.wait).until(EC.visibility_of_element_located(locator))
            return True, result
        except:
            return False, "element not found"

    def locate_element(self, locator: tuple[[], str], driver: [] = None) -> WebElement:
        """
        Locating element with wait timeout and option to mark that element
        :param locator: tuple - (By,str) - locator
        :param driver: optional - some WebElement to search inside
        :return: the element that found
        :rtype: WebElement
        """
        if driver is None:
            driver = self._driver
        try:
            element = driver.find_element(*locator)
        except TimeoutError:
            element = WebDriverWait(driver, self.wait).until(EC.presence_of_element_located(*locator))
        return element

    def locate_elements(self, locator: tuple[[], str]) -> [WebElement]:
        """
       Locating elements with wait timeout and option to mark that elements
       :param locator: tuple - (By,str) - locator
       :return: the element that found
       :rtype: [WebElement]
        """

        elements = WebDriverWait(self._driver, self.wait).until(EC.presence_of_all_elements_located(locator))
        return elements

    def locate_frame(self, locator: tuple[[], str]):
        """
       Locating frame with wait timeout
       :param locator: tuple - (By,str) - locator
        """
        try:
            self._driver.switch_to.frame(locator)
        except Exception:
            WebDriverWait(self._driver, self.wait).until(EC.frame_to_be_available_and_switch_to_it(*locator))

    def switch_to_default(self):
        """
        Switching back to default content
        """
        self._driver.switch_to.default_content()

    def script_execute(self, __script: str):
        """
        Executing given JS script
        :param __script: string of JS script
        """
        self._driver.execute_script(__script)

    def get_screenshot(self) -> bytes:
        """
        Get driver screenshot
        :return: screenshot
        :rtype: bytes
        """
        return self._driver.get_screenshot_as_png()
