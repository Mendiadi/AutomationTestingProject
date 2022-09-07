from ui_source.core.drivers.driver import Driver
from playwright.sync_api import Locator, ElementHandle, FrameLocator
import os
from ui_source.core.common.exceptions_ import LocatorWithError


class PlayWright(Driver):
    def __init__(self, driver, type_):
        super().__init__(driver, type_)

    @staticmethod
    def By(by, locator):
        if by.value == "name":
            return f"[name={locator}]"
        elif by.value == "class_name":
            return f".{locator}"
        elif by.value == "id":
            return f"id={locator}"
        elif by.value == "xpath":
            return locator
        elif by.value == "css":
            return locator
        elif by.value == "tag_name":
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

    def get_screenshot(self) -> bytes:
        """
        Get driver screenshot
        :return: screenshot
        :rtype: bytes
        """
        return self._driver.screenshot(type="png", path=os.path.join("ui_with_page_object", "img_.png"))
