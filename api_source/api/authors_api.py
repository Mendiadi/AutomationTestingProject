from api_source.api.base_api import BaseAPI
from api_source.core import rest
from api_source.models.auth_response_dto import AuthResponseDto
from api_source.api.base_api import BaseAPI
from api_source.core.constant import api_links


class Authors(BaseAPI):
    def __init__(self, url: str, headers,session):
        super().__init__(url, headers,session)

    @rest.post(data_t="json")
    def post_au(self, response):
        return rest.as_dict(response.status_code, response.text)