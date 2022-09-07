from api_source.core import rest
from api_source.models.auth_response_dto import AuthResponseDto
from api_source.api.base_api import BaseAPI


class BookApi(BaseAPI):

    def __init__(self, url: str, headers):
        super().__init__(url, headers)


    @rest.post(url='Account/register')
    def register(self,response):
        if response.ok:
            return response.text
        return rest.res_dict(response.status_code,response.text)

    @rest.post(url='Account/login')
    def login(self,response) -> AuthResponseDto:
        if response.ok:
            return AuthResponseDto(**response.json())
        return rest.res_dict(response.status_code, response.text)

    @rest.post(url='Account/refreshtoken')
    def refresh_token(self,response):
        if response.ok:
            return response.text
        return rest.res_dict(response.status_code,response.text)

