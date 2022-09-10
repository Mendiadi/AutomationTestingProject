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
# implement code start:

import requests
import enum
import logging as lg


class Req(enum.Enum):
    """
        Enum class to store REST operations

    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


# Define constant global variables

JSON = "json"
DATA = "data"


# functions starts here:

def get_session(
        headers: [] = ""
) -> requests.Session:
    """
        Return new session object
    :param headers: default nothing | the headers to current session
    :return: new session with the headers arguments
    :rtype: requests.Session
    """
    session__ = requests.session()
    session__.headers.update(headers)
    return session__


def parse_method(
        type_: Req,
        ptr__: requests.Session
) -> []:
    """
        take type and pointer to obj
        and return the function its related
    :param type_: type of request
    :param ptr__: pointer to object
    :return: function
    :rtype: function
    """
    if type_ is Req.POST:
        return ptr__.post
    elif type_ is Req.GET:
        return ptr__.get
    elif type_ is Req.DELETE:
        return ptr__.delete
    elif type_ is Req.PUT:
        return ptr__.put
    else:
        raise


def try_to_json(data):
    from api_source.models.base_model import Model
    if isinstance(data, Model):
        return data.to_json()
    return data


def get_response(
        type_: Req,
        ptr__: requests.Session,
        url: str,
        data: [],
        data_t: str
) -> requests.Response:
    """
        get the response from request session
    :param type_: type of requests see Req class
    :param ptr__: pointer to object->session
    :param url: link to send request
    :param data: data to send with request
    :param data_t: data type json or data
    :return: response object
    :rtype: requests.Response
    """
    data_temp = json_temp = None
    if data_t == JSON:
        json_temp = data
    else:
        data_temp = data
    return parse_method(type_, ptr__)(url=url, json=json_temp, data=data_temp)


def parse(
        url: str,
        kw: dict,
        param: str,
        self: []
) -> tuple:
    """
    get all data from the decorator and configure
    how its need to be sent to request
    :rtype:tuple
    """
    data = kw['data'] if "data" in kw else None
    param_ = kw[param] if param else ""
    url_ = self._base_url + url + param_ if url else self._base_url
    data = try_to_json(data)
    return data, f"{url_}/{param_}"


def request(
        type_: Req,
        url: str = None,
        param: str = None,
        data_t: str = "data"
) -> []:
    """
    Decorator with two nasted function to crate the magic function!
    the first function initial the second with same args->
    the second initial the third with same args as well->
    the third runs the first logic-> parse all data params and finally
    crate a request-> the response will update the user defined func\var
    that use this decorator properly-> and then returns user func-> then
    return second and after all of that circle the fist will return
    :param type_: type of requests see Req class
    :param url: link to send request
    :param data_t: data type json or data
    """

    def decorate(func, **kwargs) -> []:
        def wrapper(self, *args, **kwargs) -> []:
            data, url_ = parse(url, kwargs, param, self)
            self._response = get_response(type_, self._session, url_, data, data_t)
            lg.info(f'{func.__name__} -> DATA: {data}\n params: {param} RESPONSE: {self.as_dict()} ')
            return func(self)

        return wrapper

    return decorate


def get(
        url: str = None,
        param: str = None,
        data_t: str = "data"
):
    """
    Create GET request and returns the response
    :param url: url or part of it
    :param param: the user defined parameter name
    :param data_t: type of data default is "data" you can pass "json" too
    :return: response with fun that use this decorator
    :rtype: Any
    """
    return request(Req.GET, url, param, data_t)


def delete(
        url: str = None,
        param: str = None,
        data_t: str = "data"
):
    """
        Create DELETE request and returns the response
        :param url: url or part of it
        :param param: the user defined parameter name
        :param data_t: type of data default is "data" you can pass "json" too
        :return: response with fun that use this decorator
        :rtype: Any
        """
    return request(Req.DELETE, url, param, data_t)


def post(
        url: str = None,
        param: str = None,
        data_t: str = "data"
):
    """
        Create POST request and returns the response
        :param url: url or part of it
        :param param: the user defined parameter name
        :param data_t: type of data default is "data" you can pass "json" too
        :return: response with fun that use this decorator
        :rtype: Any
    """
    return request(Req.POST, url, param, data_t)


def put(
        url: str = None,
        param: str = None,
        data_t: str = "data"
):
    """
        Create PUT request and returns the response
        :param url: url or part of it
        :param param: the user defined parameter name
        :param data_t: type of data default is "data" you can pass "json" too
        :return: response with fun that use this decorator
        :rtype: Any
    """
    return request(Req.PUT, url, param, data_t)
