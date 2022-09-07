import json


class Model:

    def to_json(self) -> json:
        """
        convert object dict to json data
        :return: json dormat of object
        """

        return self.__dict__

