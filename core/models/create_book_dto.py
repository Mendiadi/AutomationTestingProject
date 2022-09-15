import dataclasses
from core.models.base_model import Model


@dataclasses.dataclass
class CreateBookDto(Model):
    name: str
    description: str
    price: float
    amountInStock: int
    imageUrl: str = None
    authorId: int = None