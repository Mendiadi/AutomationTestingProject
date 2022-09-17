import dataclasses
from core.models.base_model import Model


@dataclasses.dataclass
class AuthResponseDto(Model):
    userId: str
    token: str
    refreshToken: str

    def __post_init__(self):
        if not all(map(lambda x: isinstance(x, str), self.__dict__.values())):
            raise TypeError("the given data not string")