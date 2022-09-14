import logging

class TestAuthorPage:

    def test_author_map(self,get_main_page):
        authors_page = get_main_page.click_authors_btn()
        author = authors_page.find_author_by_name("Mark Twain")
        author_page = authors_page.go_to_author(author)
        map =author_page.get_map_cordinate()
        logging.info(map)