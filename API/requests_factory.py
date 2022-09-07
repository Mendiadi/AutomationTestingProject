import requests

class RequestsFactory:

    @staticmethod
    def get(func):
        def wrapper(*args,**kwargs):
            self = kwargs['self']
            if kwargs['data'] == "":
                kwargs['data'] = None
            response = self._session.get(url=f"{self._base_url}/{kwargs['id']}", data=kwargs['data'])
            return func(self,response=response)
        return wrapper

    @staticmethod
    def delete(func):
        def wrapper(*args, **kwargs):
            self = kwargs['self']
            if kwargs['data'] == "":
                kwargs['data'] = None
            response = self._session.delete(url=f"{self._base_url}/{kwargs['id']}", data=kwargs['data'])
            return func(self, response=response)
        return wrapper

    @staticmethod
    def post(func):
        def wrapper(*args, **kwargs):
            self = kwargs['self']
            if kwargs['data'] == "":
                kwargs['data'] = None
            response = self._session.post(url=self._base_url, data=kwargs['data'])
            return func(self, response=response)

        return wrapper

    @staticmethod
    def put(func):
        def wrapper(*args, **kwargs):
            self = kwargs['self']
            if kwargs['data'] == "":
                kwargs['data'] = None
            response = self._session.put(url=f"{self._base_url}/{kwargs['id']}", data=kwargs['data'])
            return func(self, response=response)

        return wrapper
