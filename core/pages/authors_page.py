import allure
from core.pages.base_page import BasePage
from selenium.webdriver.common.by import By


class AuthorsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    _locators = {

        "author_cont": (By.CLASS_NAME, 'author-container'),
        "author_title": (By.CLASS_NAME, 'card-title'),
        "go_to_author_btn": (By.CLASS_NAME, 'btn')
    }

    def get_authors(self):
        return self._driver.locate_elements(self._locators['author_cont'])

    def get_author_name(self, author: str) -> str:
        txt = self._driver.locate_element(self._locators['author_title'], author)
        return self._driver.text(txt)

    def find_author_by_name(self, name: str):
        authors = self.get_authors()
        for author in authors:
            if self.get_author_name(author) == name:
                return author
        return None

    def go_to_author(self, author):
        from core.pages import author_page
        if author:
            self._driver.locate_element(self._locators["go_to_author_btn"], author).click()
            return author_page.AuthorPage(self._driver)
