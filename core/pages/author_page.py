from core.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from core.pages.map_frame import MapFrame
from commons.utils import log_data
import allure


class AuthorPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    _locators = {

        "map_frame": (By.ID, 'iframeId'),
        "book_cont": (By.CLASS_NAME, 'book-container'),
        "book_title": (By.CLASS_NAME, 'card-title'),
        "book_author": (By.CLASS_NAME, 'list-group-item'),
        "book_price_cap": (By.CLASS_NAME, 'card-footer'),
        "description": (By.CLASS_NAME, 'card-text'),
        "image_url": (By.TAG_NAME, "img"),
        "headline": (By.CLASS_NAME, "badge")

    }

    def get_headline(self) -> str:
        txt = self._driver.locate_element(self._locators["headline"])
        return self._driver.text(txt)

    @allure.step("get and check books in author page")
    def get_books(self):
        books = self._driver.locate_elements(self._locators['book_cont'])
        return books

    def out_map(self, map_: MapFrame) -> ...:
        map_.__del__()
        self._driver.switch_to_default()
        log_data(msg="out from map")
        return self._driver.url

    def on_map(self) -> MapFrame:
        log_data(msg="entering to the map")
        if self._driver.type == "selenium":
            frame = self._driver.locate_element(self._locators["map_frame"])
            self._driver.locate_frame(frame)
            return MapFrame(self._driver)
        else:
            frame = self._driver.locate_frame(self._locators["map_frame"])
            return MapFrame(self._driver, frame)

    def get_book_title(self, book):
        text = self._driver.locate_element(self._locators['book_title'], book)
        txt = self._driver.text(text)
        with allure.step(f"get book title is - {txt}"):
            return txt

    def get_book(self, title: str = None):
        with allure.step(f"get the book by title = {title}"):
            books = self.get_books()
            for book in books:
                if title in self.get_book_title(book):
                    return book
            return None

    def get_book_author(self, book) -> str:
        text = self._driver.locate_element(self._locators["book_author"], book)
        txt = self._driver.text(text)
        with allure.step(f"get book author is - {txt}"):
            return txt

    def get_book_price(self, book) -> str:
        text = self._driver.locate_element(self._locators['book_price_cap'], book)
        txt = self._driver.text(text)
        txt = txt[0:txt.find("L")]
        with allure.step(f"get book price is - {txt}"):
            return txt

    def get_book_stock(self, book) -> str:
        with allure.step(f"check book stock = {book}"):
            text = self._driver.locate_element(self._locators['book_price_cap'], book)
            txt = self._driver.text(text)
            return txt[txt.find("L"):]

    @allure.step("read book description")
    def get_book_description(self, book) -> str:
        text = self._driver.locate_element(self._locators["description"], book)
        txt = self._driver.text(text)
        with allure.step(f"get book description is - {txt}"):
            return txt
