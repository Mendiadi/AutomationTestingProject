import allure
from core.api import session as se
from core.api import rest
from core.api.base_api import BaseAPI
from core.models import Author
from core.models import GetAuthorDto
from core.models import Book
from typing import Iterable
from core.api.constant import api_links

class AuthorsAPI(BaseAPI):
    def __init__(
            self,
            url: str,
            session: se.Session
    ):
        super().__init__(url, session)

    @rest.post(
        data_t=rest.JSON
    )
    def post_authors(
            self,
            author: [GetAuthorDto]
    ) -> [Author]:
        with allure.step(f"post authors from api  {author}"):
            if self._response.ok:
                return Author(**self._response.json())
            return self.as_dict(author)

    @allure.step("get authors from api")
    @rest.get()
    def get_authors(
            self
    ) -> [Iterable[Author]]:
        if self._response.ok:
            authors_list = []
            for author in self._response.json():
                author_obj = Author(**author)
                authors_list.append(author_obj)
                if author_obj.books is None:
                    pass
                else:
                    books_ = []
                    for book in author_obj.books:
                        books_.append(Book(**book.to_json()))
                    author_obj.books = books_
            return authors_list
        return self.as_dict()

    @rest.delete(
        param="id"
    )
    def delete_author(
            self,
            id: int
    ) -> dict[...]:
        with allure.step(f"delete author id={id}"):
            return self.as_dict(id)

    @rest.get(
        param="id"
    )
    def get_author_by_id(
            self,
            id: int
    ) -> [Author]:
        with allure.step(f"get author by id =  {id}"):
            if self._response.ok:
                return Author(**self._response.json())
            return self.as_dict(id)

    @rest.put(
        param="id",
        data_t=rest.JSON
    )
    def put_author_by_id(
            self,
            author: ...,
            id: int
    ) -> dict[...]:
        with allure.step(f"update author {id}"):
            return self.as_dict(author)

    @rest.get(
        url=api_links['search'],
        param="query"
    )
    def search(
            self,
            query: str
    ) -> Iterable[Author]:
        with allure.step(f"search for {query}"):
            authors = []
            for author in self._response.json():
                authors.append(Author(**author))
            return authors
