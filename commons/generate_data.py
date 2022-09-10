from faker import Faker

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

