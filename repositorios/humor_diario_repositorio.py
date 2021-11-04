from database import HumorDiario
from utilidades.data import *

class humor_diario_repositorio:

    def adicionar(self, idDiscord):
        hoje = data.hoje()
        humor = self.obter_por_id(idDiscord)

        if humor is not None:
            humor.data = hoje
            humor.save()
        else:
            HumorDiario.insert(idDiscord=idDiscord, data=hoje).execute()


    def obter_por_id(self, idDiscord):
        try:
            return HumorDiario.get(HumorDiario.idDiscord == idDiscord)
            
        except HumorDiario.DoesNotExist:
            return None

    def obter(self, idDiscord, data):
        try:
            return HumorDiario.get(
                HumorDiario.idDiscord == idDiscord,
                HumorDiario.data == data
            )
        except HumorDiario.DoesNotExist:
            return None
