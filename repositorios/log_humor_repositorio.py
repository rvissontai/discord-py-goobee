from database import LogHumor
from utilidades.data import *

class log_humor_repositorio:

    def adicionar(self, idDiscord):
        agora = data_e_hora.agora()
        LogHumor.insert(idDiscord=idDiscord, data=agora).execute()