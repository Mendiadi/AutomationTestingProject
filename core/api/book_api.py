from core.api.base_api import BaseAPI
from core.api import rest
from core.models.book import Book
from core.models.book_dto import BookDto
import allure


class BookApi(BaseAPI):
    def __init__(self, url: str, session):
        super().__init__(url, session)

    @allure.step("get books from api")
    @rest.get()
    def get_books(self) -> list[BookDto]:
        if self._response.ok:
            books = []
            for book in self._response.json():
                books.append(BookDto(**book))
            return books
        return self.as_dict()

    @rest.post(data_t=rest.JSON)
    def post_books(self, book) -> Book:
        with allure.step(f"post book: {book}"):
            if self._response.ok:
                return Book(**self._response.json())
            return self.as_dict(book)

    @rest.delete(param="id")
    def delete_book(self, id: int):
        with allure.step(f"delete book: {id}"):
            return self.as_dict()

    @rest.get(param="id")
    def get_book_by_id(self, id: int) -> BookDto:
        with allure.step(f"get book by id -> id= {id}"):
            if self._response.ok:
                return BookDto(**self._response.json())
            return self.as_dict()

    @rest.put(param="id",data_t=rest.JSON)
    def put_book(self,book,id:int):
        with allure.step(f"put book by id -> id= {id} and body = {book}"):
            return self.as_dict()