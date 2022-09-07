import requests
from API.requests_factory import RequestsFactory
from API.models.pet import Pet
class BookApi():

    def __init__(self,url:str,headers):
        self._base_url = url
        self._headers = headers
        self._session = requests.session()
        self._session.headers.update(headers)

    @RequestsFactory.post
    def post_pet(self,response:requests.Response):
        if response.ok:
            return Pet(**response.json())
        return {"code":response.status_code,"msg":response.text}

    @RequestsFactory.get
    def get_pet(self,response:requests.Response):
        if response.ok:
            return Pet(**response.json())
        return {"code":response.status_code,"msg":response.text}

    @RequestsFactory.delete
    def delete_pet(self,response:requests.Response):
        if response.ok:
            return response.text
        return {"code": response.status_code, "msg": response.text}