import dataclasses


@dataclasses.dataclass
class Pet():
    id: int
    name: str= None
    category: dict = None
    photoUrls: list= None
    tags: [str]= None
    status: str= None
