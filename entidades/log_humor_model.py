import peewee
from entidades.base_model import BaseModel

class LogHumor(BaseModel):
    id = peewee.BigIntegerField(primary_key=True, unique=True)
    idDiscord = peewee.TextField()
    data = peewee.DateTimeField()
    Resposta = peewee.TextField()
    