from api_source.models.base_model import Model
import dataclasses


@dataclasses.dataclass
class LoginDto(Model):
    email: str
    password: str
