import requests


class Rest:

    @staticmethod
    def get_session(headers) -> requests.Session:
        session__ = requests.session()
        session__.headers.update(headers)
        return session__

    @staticmethod
    def get(url=None,param=None):
        def decorate(func):
            def wrapper(self,*args,**kwargs):
                data = kwargs['data'] if "data" in kwargs else None
                param_ = kwargs[param] if param else ""
                url_ = self._base_url + url if url else self._base_url
                response = self._session.get(url=url_ + param_, data=data)
                return func(self, response=response)
            return wrapper
        return decorate

    @staticmethod
    def delete(func):
        def wrapper(self, **kwargs):

            response = self._session.delete(url=f"{self._delete_url}/{kwargs['id']}", data=kwargs['data'])

            return func(self, response=response)

        return wrapper

    @staticmethod
    def post(func):
        def wrapper(self, **kwargs):

            response = self._session.post(url=f"{self._post_url}/", data=kwargs['data'])

            return func(self, response=response)

        return wrapper

    @staticmethod
    def put(func):
        def wrapper(self, **kwargs):

            response = self._session.put(url=f"{self._put_url}/{kwargs['id']}", data=kwargs['data'])

            return func(self, response=response)


        return wrapper

    @staticmethod
    def res_dict(code, msg):
        return {"code": code, "msg": msg}