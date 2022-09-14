import allure
from core.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class StorePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    _locators = {

        "h1_label": (By.TAG_NAME, 'h1'),
        "buy_btn": (By.TAG_NAME, 'button'),
        "book_cont": (By.CLASS_NAME, 'book-container'),
        "book_title": (By.CLASS_NAME, 'card-title'),
        "book_author": (By.CLASS_NAME, 'list-group-item'),
        "book_price_cap": (By.CLASS_NAME, 'card-footer')
    }

    def get_label_h1_text(self) -> str:
        label = self._driver.locate_element(self._locators["h1_label"])
        return self._driver.text(label)

    @allure.step("get and check books")
    def get_books(self):
        books = self._driver.locate_elements(self._locators['book_cont'])
        return books

    @allure.step("check books authors")
    def get_books_by_author(self, author: str):
        books = self.get_books()
        res_list = []
        for book in books:
            if author in self.get_book_author(book):
                res_list.append(book)
        return res_list

    @allure.step("get the book")
    def get_book(self, title: str = None):
        books = self.get_books()
        for book in books:
            if title in self.get_book_title(book):
                return book
        return None

    @allure.step("check book title")
    def get_book_title(self, book):
        text = self._driver.locate_element(self._locators['book_title'], book)
        return self._driver.text(text)

    @allure.step("purchase a book")
    def purchase(self, book) -> str:

       if self._driver.type.lower() == "selenium":
            buy_btn = self._driver.locate_element(self._locators['buy_btn'], book)
            self.page_resize(0.8)
            self._driver.move_to_element(buy_btn)
            alert_var = self._driver.switch_to_alert()
            self.page_resize(1.0)
            return alert_var
       else:
            self.page_resize(0.8)
            alert_var = self._driver.switch_to_alert((book, self._locators['buy_btn']))
            self.page_resize(1.0)
            return str(alert_var.message)

    def get_book_author(self, book) -> str:
        text = self._driver.locate_element(self._locators["book_author"], book)
        return self._driver.text(text)

    @allure.step("check book price")
    def get_book_price(self, book):
        text = self._driver.locate_element(self._locators['book_price_cap'])
        return self._driver.text(text)