from core.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import allure
class SearchPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)


    _locators = {
        "book_cont": (By.CLASS_NAME, 'book-container'),
        "author_cont": (By.CLASS_NAME, 'author-container'),
        "book_title": (By.CLASS_NAME, 'card-title')
    }


    def get_book_title(self, book):
        text = self._driver.locate_element(self._locators['book_title'], book)
        txt = self._driver.text(text)
        with allure.step(f"get book title is - {txt}"):
            return txt

    def get_authors(self):
        return self._driver.locate_elements(self._locators['author_cont'])

    def get_books(self):
        return self._driver.locate_elements(self._locators['book_cont'])