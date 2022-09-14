from ui_source.core.drivers.driver import Driver
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver: Driver):
        self._driver = driver

    _common_locators = {
        "book_store_btn": (By.CLASS_NAME, 'navbar-brand'),
        "store_btn": (By.XPATH, '//*[@id="root"]/nav/div/div/a[1]'),
        "login_btn": (By.XPATH, '//*[@id="root"]/nav/div/div/a[3]')
    }

    def page_resize(self,value:float):
        self._driver.script_execute(f"document.body.style.transform='scale({value})';")

    def reload(self):
        self._driver.refresh()

    def get_store_btn_text(self)-> str:
        btn = self._driver.locate_element(self._common_locators["store_btn"])
        return self._driver.text(btn)
    def get_login_btn_text(self)-> str:
        btn = self._driver.locate_element(self._common_locators["login_btn"])
        return self._driver.text(btn)

    def get_book_store_btn_text(self)-> str:
        btn = self._driver.locate_element(self._common_locators["book_store_btn"])
        return self._driver.text(btn)

    def click_login(self):
        from ui_source.pages import login_page
        login_btn = self._driver.locate_element(self._common_locators["login_btn"])
        login_btn.click()
        return login_page.LoginPage(self._driver)

    def click_bookstore(self):
        from ui_source.pages.store_page import StorePage
        self._driver.locate_element(self._common_locators["book_store_btn"]).click()
        return StorePage(self._driver)


    @property
    def title(self) -> str:
        return self._driver.title
