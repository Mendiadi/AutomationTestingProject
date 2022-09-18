import time
import allure
from core.drivers.driver import Driver
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver: Driver):
        self._driver = driver

    _common_locators = {
        "book_store_btn": (By.CLASS_NAME, 'navbar-brand'),
        "store_btn": (By.XPATH, '//*[@id="root"]/nav/div/div/a[1]'),
        "login_btn": (By.XPATH, '//*[@id="root"]/nav/div/div/a[3]'),
        "author_btn": (By.XPATH, '//*[@id="root"]/nav/div/div/a[2]'),
        "search_bar":(By.ID,'searchtext'),
        "search_btn":(By.XPATH,'//*[@id="root"]/nav/div/form/button')

    }

    def page_resize(self, value: float):
        self._driver.script_execute(f"document.body.style.transform='scale({value})';")

    def reload(self):
        time.sleep(0.25)
        self._driver.refresh()



    def search(self,query:str):
        from core.pages.search_page import SearchPage
        with allure.step(f"search for {query}"):
            search_bar = self._driver.locate_element(self._common_locators["search_bar"])
            self._driver.send_keys(search_bar,query)
            btn = self._driver.locate_element(self._common_locators["search_btn"])
            btn.click()
            time.sleep(0.25)
            btn.click()
        return SearchPage(self._driver)

    @allure.step("click authors button")
    def click_authors_btn(self):
        from core.pages import authors_page
        self._driver.locate_element(self._common_locators['author_btn']).click()
        return authors_page.AuthorsPage(self._driver)


    def get_store_btn_text(self) -> str:
        btn = self._driver.locate_element(self._common_locators["store_btn"])
        return self._driver.text(btn)


    def get_login_btn_text(self) -> str:
        btn = self._driver.locate_element(self._common_locators["login_btn"])
        return self._driver.text(btn)


    def get_book_store_btn_text(self) -> str:
        btn = self._driver.locate_element(self._common_locators["book_store_btn"])
        return self._driver.text(btn)

    @allure.step("click login button")
    def click_login(self):
        from core.pages.login_page import LoginPage
        login_btn = self._driver.locate_element(self._common_locators["login_btn"])
        login_btn.click()
        return LoginPage(self._driver)

    @allure.step("click book store button")
    def click_bookstore(self):
        from core.pages.store_page import StorePage
        self._driver.locate_element(self._common_locators["book_store_btn"]).click()
        return StorePage(self._driver)

    @property
    def title(self) -> str:
        return self._driver.title
