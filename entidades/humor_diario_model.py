import peewee
from entidades.base_model import BaseModel

class HumorDiario(BaseModel):
    idDiscord = peewee.TextField(unique=True)
    data = peewee.DateTimeField()