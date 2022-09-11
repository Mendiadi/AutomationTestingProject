import dataclasses
from api_source.models.login_dto import LoginDto
from api_source.models.base_model import Model


@dataclasses.dataclass
class ApiUserDto(Model):
    email: str
    password: str
    firstName: str
    lastName: str

    def convert_to_login_dto_obj(self) -> LoginDto:
        return LoginDto(self.email, self.password)
