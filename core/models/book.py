import dataclasses
from core.models.base_model import Model


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

    def convert_to_book_dto(self):
        from core.models.book_dto import BookDto
        name = self.name
        description = self.description
        price = self.price
        amountInStock = self.amountInStock
        imageUrl = self.imageUrl
        authorId = self.authorId

        id = self.id
        return BookDto(name, description, price, amountInStock, imageUrl, authorId, id)
