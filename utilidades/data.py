from pytz import timezone
from datetime import datetime

class data:
    
    @staticmethod
    def hoje():
        agora = data_e_hora.agora()
        return datetime(agora.year, agora.month, agora.day)


    @staticmethod
    def final_de_semana():
        dia_da_semana = data.hoje().weekday()
        sexta_feira = 4

        if dia_da_semana > sexta_feira:
            return True
        
        return False

class data_e_hora:

    @staticmethod
    def agora():
        return datetime.now().astimezone(timezone('America/Sao_Paulo'))
