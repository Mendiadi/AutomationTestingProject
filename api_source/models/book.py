import dataclasses

from api_source.models.base_model import Model


@dataclasses.dataclass
class Book(Model):
    id: int
    name: str
    description: str
    price: float
    amountInStock: int
    imageUrl: str
    authorId: int
    author: dict
