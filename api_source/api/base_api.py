from api_source.core import rest


class BaseAPI:
    def __init__(self, url: str, session):
        self._base_url = url
        self._session = session
        self.__response = None

    def as_dict(self,code, msg):
        return {"code": code, "msg": msg}



