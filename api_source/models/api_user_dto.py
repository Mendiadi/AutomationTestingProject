import dataclasses

from api_source.models.base_model import Model
@dataclasses.dataclass
class ApiUserDto(Model):
        email:str
        password:str
        firstName:str
        lastName:str



s={"email": "adi@sela.co.il","password": "string11","firstName": "adi","lastName": "mendel"}
print(s)
print(ApiUserDto(**s).to_json())
