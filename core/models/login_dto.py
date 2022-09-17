from core.models.base_model import Model
import dataclasses


@dataclasses.dataclass
class LoginDto(Model):
    email: str
    password: str

    def __post_init__(self):
        if not all(map(lambda x: isinstance(x, str), self.__dict__.values())):
            raise TypeError("the given data not string")