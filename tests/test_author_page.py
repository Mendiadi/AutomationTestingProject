import logging
import time

import allure


@allure.epic("UI Author Page")
class TestAuthorPage:




    def test_validate_books(self):
        pass

    def test_validate_name_headline(self):
        pass

    def test_validate_data_vs_database(self):
        pass

    def validate_data_updated_in_books(self):
        pass

    def test_add_and_delete_books(self):
        pass

    def test_validate_home_location_updated(self):
        pass

    def test_validate_map(self,get_main_page):
        authors_page = get_main_page.click_authors_btn()
        author = authors_page.find_author_by_name("Mark Twain")
        author_page = authors_page.go_to_author(author)
        map = author_page.on_map()
        map_cor = map.get_map_cordinate()
        logging.info(map_cor)
        map.change_look_style()
        time.sleep(5)
        author_page.out_map(map)


