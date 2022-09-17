class BaseAPI:
    def __init__(self, url: str, session:...):
        self._base_url = url
        self._session = session.session
        self._response = None

    def as_dict(self, obj:...=None) -> dict[str,...]:
        return {"code": self._response.status_code,
                "reason": self._response.reason,
                "msg": self._response.text, "obj": obj}


    def __str__(self) -> str:
        return f"API {self._base_url} service"