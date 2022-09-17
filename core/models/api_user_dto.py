import dataclasses
from core.models import LoginDto
from core.models.base_model import Model


@dataclasses.dataclass
class ApiUserDto(Model):
    email: str
    password: str
    firstName: str
    lastName: str

    def __post_init__(self):
        if not all(map(lambda x: isinstance(x, str), self.__dict__.values())):
            raise TypeError("the given data not string")

    def convert_to_login_dto_obj(self) -> LoginDto:
        return LoginDto(self.email, self.password)

