import math

from faker import Faker
from api_source.models.api_user_dto import ApiUserDto
from api_source.models.create_author_dto import CreateAuthorDto


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

    def generate_author(self) -> CreateAuthorDto:
        name = self.firstname() + self.lastname()
        homelo = self._faker.random.randint(-180, 180)
        homala = self._faker.random.randint(-90, 90)
        homala *= math.sin(homala)
        homelo *= math.sin(homelo)
        return CreateAuthorDto(name, homala, homelo)
