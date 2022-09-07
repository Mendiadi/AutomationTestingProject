from api_source.core import rest
from api_source.models.pet import Pet
from api_source.api.base_api import BaseAPI


class BookApi(BaseAPI):

    def __init__(self, url: str, headers):
        super().__init__(url, headers)

    @rest.post()
    def post_pet(self, response):
        if response.ok:
            return Pet(**response.json())
        return rest.res_dict(response.status_code, response.text)


    @rest.get(param="id")
    def get_pet(self, response):
        if response.ok:
            return Pet(**response.json())
        return rest.res_dict(response.status_code, response.text)


    @rest.delete(param="id")
    def delete_pet(self, response):
        return rest.res_dict(response.status_code, response.text)


    @rest.get(url='findByStatus?status=',param="status")
    def find_by_status(self,response):

        if response.ok:
            pet_list = []
            for pet in response.json():
                pet_list.append(Pet(**pet))
            return pet_list
        return rest.res_dict(response.status_code, response.text)



    @rest.put()
    def put_pet(self,response):
        if response.ok:
            return Pet(**response.json())
        return rest.res_dict(response.status_code, response.text)