import datetime

from database import HumorDiario

class humor_diario_repositorio:

    def adicionar(self, idDiscord):
        hoje = datetime.date.today()
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
