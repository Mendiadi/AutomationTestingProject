import math

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

    def generate_author(self, name: str = None) -> CreateAuthorDto:
        name = name if name else self.firstname() + self.lastname()
        homelo = self._faker.random.randint(-180, 180)
        homala = self._faker.random.randint(-90, 90)
        homala *= math.sin(homala)
        homelo *= math.sin(homelo)
        return CreateAuthorDto(name, homala, homelo)

    def generate_book(self, authorid=None, price=None, amount=None, description: str = None,
                      name: str = None) -> CreateBookDto:
        book = {
            "name": name if name else self._faker.name(),
            "description": description if description else "description",
            "price": price if price else 50,
            "amountInStock": amount if amount else 10,
            "imageUrl": self._faker.url(),
            "authorId": authorid if authorid else self._faker.random.randint(4, 200)
        }
        return CreateBookDto(**book)
