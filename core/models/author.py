import dataclasses
from core.models import book
from core.models.base_model import Model


@dataclasses.dataclass
class Author(Model):
    id: int
    name: str
    homeLatitude: float
    homeLongitude: float
    books: [book.Book] = None

    def __eq__(self, other):
        if isinstance(other,str):
            return other == self.name
        return (self.id == other.id) and \
               (self.name == other.name) and \
               (self.homeLatitude == other.homeLatitude) and \
               (self.homeLongitude == other.homeLongitude)
