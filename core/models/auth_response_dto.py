import dataclasses
from core.models.base_model import Model


@dataclasses.dataclass
class AuthResponseDto(Model):
    userId: str
    token: str
    refreshToken: str
