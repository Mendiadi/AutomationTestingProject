import logging
import allure
import pytest

LOGGER = logging.getLogger(__name__)

@pytest.mark.smoke
class TestSmoke:

    @allure.title("verify open page")
    def test_page_open(self, get_main_page):
        LOGGER.info(f"executing test case: search valid")
        excepted_title = "React App"
        LOGGER.info(f"actual: {get_main_page.title} | excepted: {excepted_title}")
        assert get_main_page.title == excepted_title

    @allure.title("sanity login page nad register load properly")
    def test_login_page_loading_elements(self,get_main_page):
        login_result = get_main_page.elements_visible_login()
        register_page = get_main_page.click_register()
        register_result = register_page.element_visible_register()
        results = (register_result,login_result)
        for result in results:
            for element_is_found,msg in result:
                LOGGER.info(f"{element_is_found} | {msg}")
                assert element_is_found



    def test_store_element_loading(self,get_main_page):
        pass

    def test_authors_element_loading(self,get_main_page):
        pass

    def test_authors_page_loading_elements(self):
        pass

    def test_base_page_load_element(self):
        pass



