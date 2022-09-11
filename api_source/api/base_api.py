class BaseAPI:
    def __init__(self, url: str, session):
        self._base_url = url
        self._session = session
        self._response = None

    def as_dict(self, obj=None):
        return {"code": self._response.status_code, "msg": self._response.text, "obj": obj}
