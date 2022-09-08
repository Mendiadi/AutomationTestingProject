"""
    Written by adi mendel 6.8.2022
    my implementation for rest api using decorator factory.
    you can send requests from your api class using my decorators as
    @rest.get() - for get request
    @rest.post() for post request
    @rest.delete() for delete request
    @rest.put() for put request
    to use it properly you need to attention for some details!
    (1) you need in your api class method calls to give only one parameter as name 'response' (self also include)
    example (1): in your api class :
                SomeApi():
                    def __init__(self):
                        pass

                    @rest.post()
                    def post_user(self,response):
                        return response # to return the result or return any manipulation
    (2) you can pass the url or just part of it using url param config like that:
    example (2):
            SomeApi():
                def __init__(self):
                    pass

                @rest.post(url="myUrl") # as you can see you can config url
                def post_user(self,response):
                    return response # to return the result or return any manipulation
    (3) also you can config the params to the url mostly like this:
        SomeApi():
                def __init__(self):
                    pass

                @rest.post(url="myUrl",param="name")
                def post_user_name(self,response):
                    return response # to return the result or return any manipulation

                @rest.post(url="myUrl",param="id")
                def post_user_id(self,response):
                    return response # to return the result or return any manipulation

        ** in your test file you use it like:
            def test_user():
                res = post_user_name(name="sample")
                res = post_user_id(id="sample")
                # as you can see you can call these api methods and -
                use the parameter config to send most you need to.

    (4) you can always send data with your request
    example (4):
        in your test file -
            def test_user():
                res = post_user(data={name:name,id:id})

                # as you can see you can always send or ignore and then data will be None

    (5) you can choose if you send data by "data=" or "json=" using the data_t arg:
    example (5):
            @rest.post(data_t="json") # for json, its will be default "data" if not sending anything
            def post_user_id(self,response):
                return response # to return the result or return any manipulation

    after im showed you how to use it and example also
    you can simply try and use it its very cool decorators.

    more will come out soon, adi.
"""

import requests

GET = "GET"
POST = "POST"
PUT = "PUT"
DELETE = "DELETE"


def get_session(headers="") -> requests.Session:
    session__ = requests.session()
    session__.headers.update(headers)
    return session__


def get_response(type, ptr__, url, data, data_t):
    if type is POST:
        return ptr__.post(url=url, json=data) if data_t == "json" else ptr__.post(url=url, data=data)
    elif type is GET:
        return ptr__.post(url=url, json=data) if data_t == "json" else ptr__.post(url=url, data=data)
    elif type is DELETE:
        return ptr__.post(url=url, json=data) if data_t == "json" else ptr__.post(url=url, data=data)
    elif type is PUT:
        return ptr__.post(url=url, json=data) if data_t == "json" else ptr__.post(url=url, data=data)
    else:
        raise


def parse(url, kw, param, self):
    data = kw['data'] if "data" in kw else None
    param_ = kw[param] if param else ""
    url_ = self._base_url + url if url else self._base_url
    return data, param_, url_


def request(type_, url=None, param=None, data_t="data"):
    def decorate(func, **kwargs):
        def wrapper(self, *args, **kwargs):
            data, param_, url_ = parse(url, kwargs, param, self)
            response = get_response(type_, self._session, url_, data, data_t)
            return func(self, response=response)

        return wrapper

    return decorate


def get(url=None, param=None, data_t="data"):
    return request(GET, url, param, data_t)


def delete(url=None, param=None, data_t="data"):
    return request(DELETE, url, param, data_t)


def post(url=None, param=None, data_t="data"):
    return request(POST, url, param, data_t)


def put(url=None, param=None, data_t="data"):
    return request(PUT, url, param, data_t)


def as_dict(code, msg):
    return {"code": code, "msg": msg}
