import math
from commons import images
from faker import Faker
from core.models import ApiUserDto
from core.models.create_author_dto import CreateAuthorDto
from core.models import CreateBookDto


class RandomData:
    def __init__(self):
        self._faker = Faker()

    def email(self) -> str:
        return self._faker.email()

    def password(self) -> str:
        return self._faker.password()

    def firstname(self) -> str:
        return self._faker.name().split(' ')[0]

    def lastname(self) -> str:
        return self._faker.name().split(' ')[1]

    def generate_account(self) -> ApiUserDto:
        user = {
            "email": self.email(),
            "password": self.password(),
            "firstName": self.firstname(),
            "lastName": self.lastname()
        }
        while len(user['password']) not in range(4, 15):
            user['password'] = self.password()
        return ApiUserDto(**user)

    def generate_author(
            self,
            name: str = None
            ,la:float=None
            ,lo:float=None
    ) -> CreateAuthorDto:
        name = name if name else self.firstname() + self.lastname()
        homelo = self._faker.random.randint(-180, 180) if not lo else lo
        homala = self._faker.random.randint(-90, 90) if not la else la
        homala *= math.sin(homala)
        homelo *= math.sin(homelo)
        return CreateAuthorDto(name, homala, homelo)

    def generate_book(
            self,
            authorid:int=None,
            price: int = None,
            amount: int = None,
            description: str = None,
            name: str = None,
            imageUrl: str = None
    ) -> CreateBookDto:
        if price is None:
            price = 10
        if amount is None:
            amount = 10
        book = {
            "name": name if name else self._faker.name(),
            "description": description if description else "description",
            "price": price,
            "amountInStock": amount,
            "imageUrl": images.IMAGES[self._faker.random.randint(0, len(images.IMAGES) - 1)] if imageUrl else None,
            "authorId": authorid if authorid else self._faker.random.randint(4, 200)
        }
        return CreateBookDto(**book)

    @staticmethod
    def image_temp() -> str:
        return images.img_temp
