from pytz import timezone
from datetime import datetime

class data:
    
    @staticmethod
    def agora():
        return datetime.now().astimezone(timezone('America/Sao_Paulo'))
