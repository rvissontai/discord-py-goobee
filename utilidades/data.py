from pytz import timezone
from datetime import datetime

class data:
    
    @staticmethod
    def hoje():
        agora = data_e_hora.agora()
        return datetime(agora.year, agora.month, agora.day)

class data_e_hora:

    @staticmethod
    def agora():
        return datetime.now().astimezone(timezone('America/Sao_Paulo'))
