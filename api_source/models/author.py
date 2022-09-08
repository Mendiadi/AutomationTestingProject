import dataclasses

from api_source.models.base_model import Model

@dataclasses.dataclass
class Author(Model):
    id:int
    name:str
    homeLatitude :float
    homeLongitude: float
    books: [] = None
