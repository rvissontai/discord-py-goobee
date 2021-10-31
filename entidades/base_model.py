import os
import peewee
from peewee import PostgresqlDatabase

#banco = peewee.SqliteDatabase('database.db')
banco = PostgresqlDatabase(
    os.getenv('POSTGRE-DATABASE'),
    user=os.getenv('POSTGRE-USER'),
    password=os.getenv('POSTGRE-PASS'), 
    host=os.getenv('POSTGRE-HOST'), 
    port=5432)

class BaseModel(peewee.Model):
    class Meta:
        # Indica em qual banco de dados a tabela
        # sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente
        database = banco