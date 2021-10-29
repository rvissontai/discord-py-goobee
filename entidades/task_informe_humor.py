import peewee
from entidades.base_model import BaseModel

class TaskInformeHumor(BaseModel):
    data = peewee.DateTimeField()