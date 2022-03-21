import peewee
from entidades.base_model import BaseModel

class TaskInformeDaily(BaseModel):
    data = peewee.DateTimeField()