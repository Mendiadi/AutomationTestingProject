from ui_source.core.drivers.driver import Driver
from playwright.sync_api import Locator, ElementHandle, FrameLocator
from ui_source.core.exceptions_ import LocatorWithError
import os
import allure
from allure_commons.types import AttachmentType


class PlayWright(Driver):
    def __init__(self, driver, type_):
        super().__init__(driver, type_)

    def switch_to_alert(self, input__=None):
        btn = input__[0].query_selector(self.By(*input__[1]))
        with self._driver.expect_event("dialog") as dialog:
            self._driver.on("dialog", lambda dialog: dialog.accept())
            btn.click()
            dialog.is_done()
            txt = dialog.value

            return txt

    def element_is_visible(self, locator):
        return self._driver.is_visible(self.By(*locator)), "locator"

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
        except:
            element = driver.query_selector(self.By(*locator))
        finally:
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

    def locate_frame(self, locator: tuple) -> FrameLocator:
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
