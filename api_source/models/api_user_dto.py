import dataclasses

from api_source.models.base_model import Model


@dataclasses.dataclass
class ApiUserDto(Model):
    email: str
    password: str
    firstName: str
    lastName: str



