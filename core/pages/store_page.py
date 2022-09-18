import time
import allure
from core.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from commons.utils import log_data
import threading


class StorePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self._scanner = None

        self._purchase_msg = ""
        self._kill = False

    _locators = {

        "h1_label": (By.TAG_NAME, 'h1'),
        "buy_btn": (By.TAG_NAME, 'button'),
        "book_cont": (By.CLASS_NAME, 'book-container'),
        "book_title": (By.CLASS_NAME, 'card-title'),
        "book_author": (By.CLASS_NAME, 'list-group-item'),
        "book_price_cap": (By.CLASS_NAME, 'card-footer'),
        "description": (By.CLASS_NAME, 'card-text'),
        "image_url": (By.TAG_NAME, "img")
    }

    def _scan_for_alerts(self):
        keep_going = True
        start = time.time()
        end = 0
        while end - start < 1.5 and keep_going:
            try:
                self._purchase_msg = self._driver.switch_to_alert()
                keep_going = False
            except Exception as e:
                log_data(e)
                time.sleep(0.25)
            end = time.time()

    def _scanner_(self):
        if self._scanner is None:
            self._scanner = threading.Thread(target=self._scan_for_alerts)
            self._scanner.setDaemon(True)
        if not self._scanner.is_alive():
            self._scanner.start()
            self._scanner.join(1)
            self._kill = True

    def get_label_h1_text(self) -> str:
        label = self._driver.locate_element(self._locators["h1_label"])
        return self._driver.text(label)

    @allure.step("get and check books")
    def get_books(self):
        books = self._driver.locate_elements(self._locators['book_cont'])
        return books

    def get_books_by_author(self, author: str):
        with allure.step(f"check books by author {author}"):
            books = self.get_books()
            res_list = []
            for book in books:
                if author in self.get_book_author(book):
                    res_list.append(book)
            return res_list

    @allure.step("get book img url")
    def get_book_image_url(self, book) -> str:
        img = self._driver.locate_element(self._locators['image_url'], book)
        return self._driver.get_attribute(img, "src")

    def get_book(self, title: str = None):
        with allure.step(f"get the book by title = {title}"):
            books = self.get_books()
            for book in books:
                if title in self.get_book_title(book):
                    return book
            return None

    def get_book_title(self, book):
        text = self._driver.locate_element(self._locators['book_title'], book)
        txt = self._driver.text(text)
        with allure.step(f"get book title is - {txt}"):
            return txt

    def _purchase_handler(self, book):
        if self._driver.type.lower() == "selenium":
            buy_btn = self._driver.locate_element(self._locators['buy_btn'], book)
            try:
                self._driver.move_to_element(buy_btn)
                self._purchase_msg = self._driver.switch_to_alert()
            except:
                self.page_resize(0.8)
                buy_btn.click()
                self._purchase_msg = self._driver.switch_to_alert()
        else:
            self.page_resize(0.8)
            self._purchase_msg = str(self._driver.switch_to_alert((book, self._locators['buy_btn'])))

    def purchase(self, book) -> str:
        book_name = self.get_book_title(book)
        log_data(book_name, msg="purchase book title= ")
        with allure.step(f"purchase {book_name} from the store"):
            self._purchase_handler(book)
            if not self._kill:

                self._scanner_()
            log_data(self._purchase_msg)
            return self._purchase_msg

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
    def get_book_decription(self, book) -> str:
        text = self._driver.locate_element(self._locators["description"], book)
        txt = self._driver.text(text)
        with allure.step(f"get book decription is - {txt}"):
            return txt


