import time

from core.drivers import Driver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import selenium.common.exceptions as se
from commons.utils import log_data


class Selenium(Driver):
    def __init__(self, driver, type_):
        self.wait = 15
        super().__init__(driver, type_)

    def switch_to_alert(self, input__=""):
        alert_var = self._driver.switch_to.alert
        t = alert_var.text
        alert_var.accept()
        return t

    def move_to_element(self, element):
        try:
            actions = ActionChains(self._driver)
            actions.scroll_to_element(element)
            element.click()
        except Exception as e:
            log_data(e)
            actions.move_to_element(element)

    def element_is_visible(self, locator):
        try:
            result = WebDriverWait(self._driver, self.wait).until(EC.visibility_of_element_located(locator))
            return result.is_displayed()
        except Exception as e:
            log_data(f"log msg from Driver - {e}")
            return False

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
        except (se.TimeoutException, se.NoSuchElementException, se.ElementNotVisibleException) as e:
            log_data(f"log msg from Driver - {e}")

            element = WebDriverWait(driver, self.wait).until(EC.presence_of_element_located(locator))
        except (se.StaleElementReferenceException, se.TimeoutException) as e:
            log_data(f"log msg from Driver - {e}")
            time.sleep(0.5)
            self.refresh()
            element = driver.find_element(*locator)
        return element

    def switch_to_tab(self, val: int):
        if len(self._driver.window_handles) > 1:
            self._driver.window_handles.pop()
            self._driver.switch_to.window(self._driver.window_handles[val])
        return val

    def get_attribute(self, element, name: str) -> [str]:
        return element.get_attribute(name)

    def url(self) -> str:
        return self._driver.current_url

    def locate_elements(self, locator: tuple[[], str]) -> [WebElement]:
        """
       Locating elements with wait timeout and option to mark that elements
       :param locator: tuple - (By,str) - locator
       :return: the element that found
       :rtype: [WebElement]
        """
        try:

            elements = WebDriverWait(self._driver, self.wait).until(EC.presence_of_all_elements_located(locator))
        except Exception as e:
            log_data(e)
            time.sleep(0.5)
            self.refresh()
            elements = WebDriverWait(self._driver, self.wait).until(EC.presence_of_all_elements_located(locator))
        return elements

    def locate_frame(self, locator: tuple[[], str]):
        """
       Locating frame with wait timeout
       :param locator: tuple - (By,str) - locator
        """
        try:
            self._driver.switch_to.frame(locator)
        except Exception as e:
            log_data(f"log msg from Driver - {e}")
            self._driver.switch_to.frame(locator)

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
