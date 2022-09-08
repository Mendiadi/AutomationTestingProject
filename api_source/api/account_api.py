from api_source.core import rest
from api_source.models.auth_response_dto import AuthResponseDto
from api_source.api.base_api import BaseAPI
from api_source.core.constant import api_links



class AccountApi(BaseAPI):

    def __init__(self, url: str, headers,session):
        super().__init__(url, headers,session)

    @rest.post(url=api_links["register"],data_t="json")
    def register(self, response):
        return rest.as_dict(response.status_code, response.text)

    @rest.post(url=api_links['login'],data_t="json")
    def login(self, response) -> AuthResponseDto:
        if response.ok:
            return AuthResponseDto(**response.json())
        return rest.as_dict(response.status_code, response.text)

    @rest.post(url=api_links['token'],data_t="json")
    def refresh_token(self, response):
        if response.ok:
            return response.text
        return rest.as_dict(response.status_code, response.text)

