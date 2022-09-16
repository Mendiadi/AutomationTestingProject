import dataclasses
from core.models.base_model import Model


@dataclasses.dataclass
class BookDto(Model):
    name: str
    description: str
    price: float
    amountInStock: int
    imageUrl: str
    authorId: int
    # maximum: 2147483647
    # minimum: 1
    id: int
