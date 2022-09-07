from __future__ import annotations
from dataclasses import dataclass
from ui_source.core.common.constant import *
import json
from ui_source.core.common.exceptions_ import *


@dataclass
class TestsData:
    """
    Store the initial data for the test that reading from init.json config file.
    """
    url: str
    email: str
    password: str
    browser: str
    lib: str
    driver_path: str


    def valid(self):
        if not isinstance(self.url, str):
            raise TypeError(f"url that given in init.json file are {type(self.url)} but needs to be str")
        if not isinstance(self.email, str):
            raise TypeError(f"email that given in init.json file are {type(self.email)} but needs to be str")
        if not isinstance(self.password, str):
            raise TypeError(f"password that given in init.json file are {type(self.password)} but needs to be str")
        if not isinstance(self.browser, str):
            raise TypeError(f"browser that given in init.json file are type  {type(self.url)} but needs to be str")
        if self.browser not in BROWSERS:
            raise BrowserNotSupport(f"Browser {self.browser} is unrecognized. must be {CHROME} or {FIREFOX}")
        if self.lib not in LIBS:
            raise LibNotSupport(f"lib {self.lib} is unrecognized. must be {PLAYWRIGHT} or {SELENIUM}")



    @staticmethod
    def load(path: str) -> TestsData:
        """
        load and read the file and
        return data object
        :param path: path to json file
        :return: object with the data
        :rtype: TestsData
        """
        try:
            with open(path, "r") as json_file:
                json_file = json.load(json_file)
        except FileNotFoundError:
            with open(rf"{PACKAGE_NAME}\{path}", "r") as json_file:
                json_file = json.load(json_file)

        return TestsData(**json_file)


def  load_test_data():
    return TestsData.load(DATA_FILE)