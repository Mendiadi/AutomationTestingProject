import dataclasses

from api_source.models.base_model import Model


@dataclasses.dataclass
class Author(Model):
    id: int
    name: str
    homeLatitude: float
    homeLongitude: float
    books: [] = None

    def __eq__(self, other):
        return (self.id == other.id) and \
               (self.name == other.name) and \
               (self.homeLatitude == other.homeLatitude) and \
               (self.homeLongitude == other.homeLongitude)
