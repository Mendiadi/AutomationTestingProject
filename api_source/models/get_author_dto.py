
from api_source.models.base_model import Model

class GetAuthorDto(Model):
    name:str
    homeLatitude:float
    homeLongitude:float
    id:int
