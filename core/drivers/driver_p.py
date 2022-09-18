import time
from core.drivers import Driver
from playwright.sync_api import Locator, ElementHandle, FrameLocator
from commons import LocatorWithError
from commons.utils import log_data
import os



class PlayWright(Driver):
    def __init__(self, driver, type_):
        super().__init__(driver, type_)
        self._driver_temp = None
        self._dialog_msg_temp = None

    def switch_to_alert(self, input__=None):
        btn = input__[0].query_selector(self.By(*input__[1]))
        def on_dialog(dialog):
            self._dialog_msg_temp = dialog.message
            dialog.accept()
        self._driver.on("dialog",on_dialog)
        btn.click()
        return self._dialog_msg_temp


    def switch_to_tab(self, val: int):
        log_data(msg=" switching tab current url" + self._driver.url)
        pages = self._driver.context.pages
        if len(self._driver.context.pages) > 1:
            self._driver = pages[val]
        return val

    def get_attribute(self, element, name: str) -> [str]:
        return element.get_attribute(name)


    def url(self) -> str:
        return self._driver.url

    def element_is_visible(self, locator):
        return self._driver.is_visible(self.By(*locator))

    def move_to_element(self, element):

        try:
            self._driver.hover(element)
        except Exception as e:
            log_data(e)
            return

    @staticmethod
    def By(by, locator):
        if by == "name":
            return f"[name={locator}]"
        elif by == "class name":
            return f".{locator}"
        elif by == "id":
            return f"id={locator}"
        elif by == "xpath":
            return locator
        elif by == "css selector":
            return locator
        elif by == "tag name":
            return locator
        else:
            raise LocatorWithError("unsolved With value given.")

    def locate_element(self, locator: tuple, driver: [] = None) -> [Locator, ElementHandle]:
        """
        Locating element with wait timeout and option to mark that element
        :param locator: tuple - (By,str) - locator
        :param driver: optional - some WebElement to search inside
        :return: the element that found
        :rtype: Locator
        """
        if driver is None:
            driver = self._driver

        try:
            element = driver.locator(self.By(*locator))
        except AttributeError as e:
            log_data(f"log msg from Driver - {e}")
            element = driver.query_selector(self.By(*locator))
        except Exception as e:
            log_data(e)
            self._driver.reload()
            element = self._driver.query_selector(self.By(*locator))
        return element

    def locate_elements(self, locator: tuple) -> [ElementHandle]:
        """
       Locating elements with wait timeout and option to mark that elements
       :param locator: tuple - (By,str) - locator
       :return: the element that found
       :rtype: [ElementHandle]
        """
        # if self._driver.is_visible(locator, timeout=wait):

        elements = self._driver.query_selector_all(self.By(*locator))

        return elements
        # else:
        #     raise TimeoutError

    def switch_to_default(self):
        pass

    def locate_frame(self, locator: tuple):
        """
        Locate frame
        :param locator: frame locator
        :return: frame
        :rtype: FrameLocator
        """

        frame = self._driver.frame_locator(self.By(*locator))

        return frame

    def script_execute(self, __script: str):
        """
        Executing given JS script
        :param __script: string of JS script
        """
        self._driver.evaluate(__script)

    def get_screenshot(self):
        """
        Get driver screenshot
        :return: screenshot
        :rtype: bytes
        """
        image = f"img.png"
        if "reports" in os.listdir('/practice_automation'):
            img__ = self._driver.screenshot(
                path=fr"{image}")
            return img__

    def alert(self):
        self._driver.on("dialog", lambda dialog: dialog.accept())
