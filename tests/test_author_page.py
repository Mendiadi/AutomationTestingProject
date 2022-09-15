import logging
import time

import allure
import pytest


@allure.epic("UI Author Page")
class TestAuthorPage:




    def test_validate_books(self):
        pytest.skip()
        pass

    def test_validate_name_headline(self):
        pytest.skip()
        pass

    def test_validate_data_vs_database(self):
        pytest.skip()
        pass

    def validate_data_updated_in_books(self):
        pytest.skip()
        pass

    def test_add_and_delete_books(self):
        pytest.skip()
        pass

    def test_validate_home_location_updated(self):
        pytest.skip()
        pass

    def test_validate_map_cordinate(self,get_main_page,authors_api):
        authors_page = get_main_page.click_authors_btn()
        author = authors_page.find_author_by_name("George Orwell")
        author_page = authors_page.go_to_author(author)
        map = author_page.on_map()
        la,lo = map.get_map_cordin_in_float()
        author_page.out_map(map)
        author = authors_api.get_author_by_id(id=1)
        logging.info(f"{la},{lo}")

        assert author.homeLatitude == la
        assert author.homeLongitude == lo

    def test_map_change_look(self,get_main_page):
        authors_page = get_main_page.click_authors_btn()
        author = authors_page.find_author_by_name("George Orwell")
        author_page = authors_page.go_to_author(author)
        map = author_page.on_map()
        map_cor = map.get_map_details()
        logging.info(map_cor)
        change_look_style = map.change_look_style()
        assert change_look_style != "Show street map"
        change_look_style_again = map.change_look_style()
        assert change_look_style_again != "Show satellite imagery"



