from ui_source.core.drivers.driver import Driver
from ui_source.core.drivers.supports import With

class BasePage:
    def __init__(self, driver: Driver):
        self._driver = driver

    _common_locators = {
        "book_store_btn": (With.CLASS_NAME,'navbar-brand'),
        "store_btn":(With.XPATH,'//*[@id="root"]/nav/div/div/a[1]'),
        "login_btn":(With.XPATH,'//*[@id="root"]/nav/div/div/a[3]')
    }

    def click_login(self):
        from ui_source.pages import login_page
        login_btn = self._driver.locate_element(self._common_locators["login_btn"])
        login_btn.click()
        return login_page.LoginPage(self._driver)

    def click_bookstore(self):
        self._driver.locate_element(self._common_locators["book_store_btn"]).click()

    @property
    def title(self) -> str:
        return self._driver.title
