import pytest

from api_source.core import rest
from api_source.models.auth_response_dto import AuthResponseDto
from api_source.api.base_api import BaseAPI
from api_source.core.constant import api_links

# api_link = utils.api_url("api_manage.yaml")

class BookApi(BaseAPI):

    def __init__(self, url: str, headers):
        super().__init__(url, headers)


    @rest.post(url=api_links["register"])
    def register(self,response):
        return rest.res_dict(response.status_code,response.text)



    @rest.post(url=api_links['login'])
    def login(self,response) -> AuthResponseDto:
        if response.ok:
            return AuthResponseDto(**response.json())
        return rest.res_dict(response.status_code, response.text)

    @rest.post(url=api_links['token'])
    def refresh_token(self,response):
        if response.ok:
            return response.text
        return rest.res_dict(response.status_code,response.text)

