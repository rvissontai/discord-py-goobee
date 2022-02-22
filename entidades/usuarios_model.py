import peewee
from entidades.base_model import BaseModel

class Usuarios(BaseModel):
    id = peewee.BigIntegerField(primary_key=True, unique=True, constraints=[peewee.SQL('AUTO_INCREMENT')])
    idDiscord = peewee.TextField(unique=True)
    login = peewee.TextField()
    senha = peewee.TextField()