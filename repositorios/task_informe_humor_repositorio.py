from database import TaskInformeHumor
from utilidades.data import data

class task_informe_humor_repositorio:

    def adicionar(self):
        hoje = data.hoje()
        task = self.obter()

        if task is not None:
            task.data = hoje
            task.save()
        else:
            TaskInformeHumor.insert(data=hoje).execute()


    def obter_por_data(self, data):
        try:
            return TaskInformeHumor.get(TaskInformeHumor.data == data)
            
        except TaskInformeHumor.DoesNotExist:
            return None

    def obter_hoje(self):
        try:
            return TaskInformeHumor.get(TaskInformeHumor.data == data.hoje())
            
        except TaskInformeHumor.DoesNotExist:
            return None

    def obter(self):
        try:
            return TaskInformeHumor.get()
        except TaskInformeHumor.DoesNotExist:
            return None