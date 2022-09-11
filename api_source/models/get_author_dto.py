import dataclasses

from api_source.models.base_model import Model
@dataclasses.dataclass
class GetAuthorDto(Model):
    name:str
    homeLatitude:float
    homeLongitude:float
    id:int

    @staticmethod
    def create_from_author(other):
        return GetAuthorDto(other.name,other.homeLatitude,other.homeLongitude,other.id)