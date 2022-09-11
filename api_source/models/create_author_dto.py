import dataclasses

from api_source.models.base_model import Model
@dataclasses.dataclass
class CreateAuthorDto(Model):
    name:str
    homeLatitude:float
    homeLongitude:float
