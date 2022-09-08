from api_source.api.base_api import BaseAPI
from api_source.core import rest
from api_source.models.auth_response_dto import AuthResponseDto
from api_source.api.base_api import BaseAPI
from api_source.core.constant import api_links
from api_source.models.author import Author


class AuthorsApi(BaseAPI):
    def __init__(self, url: str, session):
        super().__init__(url, session)

    @rest.post(data_t=rest.JSON)
    def post_authors(self, response):
        if response.ok:
            return Author(**response.json())
        return self.as_dict(response.status_code, response.text)

    @rest.get()
    def get_authors(self, response):
        if response.ok:
            authors_list = []
            for author in response.json():
                authors_list.append(Author(**author))
            return authors_list
        return self.as_dict(response.status_code, response.text)

    @rest.delete(param="id")
    def delete_author(self, response):
        return self.as_dict(response.status_code, response.text)
