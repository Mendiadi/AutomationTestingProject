import dataclasses
from core.models.base_model import Model


@dataclasses.dataclass
class CreateAuthorDto(Model):
    name: str
    homeLatitude: float
    homeLongitude: float
