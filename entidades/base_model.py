import peewee

banco = peewee.SqliteDatabase('database.db')

class BaseModel(peewee.Model):
    class Meta:
        # Indica em qual banco de dados a tabela
        # sera criada (obrigatorio). Neste caso,
        # utilizamos o banco 'codigo_avulso.db' criado anteriormente
        database = banco