import peewee 
from entidades.barrel import *

def iniciar_database():
    try:
        Usuarios.create_table()

        Configuracao.create_table()

        HumorDiario.create_table()

        TaskInformeHumor.create_table()

        print("Banco de dados está pronto.")
    except peewee.OperationalError:
        print("Não foi possível iniciar o banco!")