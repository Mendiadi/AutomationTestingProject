from api_source.core.requests_factory import Rest
from api_source.models.pet import Pet
from api_source.api import base_api


class BookApi(base_api.BaseAPI):

    def __init__(self, url: str, headers):
        super().__init__(url, headers)

    @Rest.post
    def post_pet(self, response):
        if response.ok:
            return Pet(**response.json())
        return Rest.res_dict(response.status_code, response.text)


    @Rest.get
    def get_pet(self, response):
        if response.ok:
            return Pet(**response.json())
        return Rest.res_dict(response.status_code, response.text)


    @Rest.delete
    def delete_pet(self, response):
        return Rest.res_dict(response.status_code, response.text)

