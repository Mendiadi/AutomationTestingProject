import dataclasses

from api_source.models.base_model import Model
@dataclasses.dataclass
class AuthResponseDto(Model):
    userId:str
    token:str
    refreshToken:str