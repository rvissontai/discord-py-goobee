from database import TaskInformeDaily
from utilidades.data import data

class task_informe_daily_repositorio:

    def adicionar(self):
        hoje = data.hoje()
        task = self.obter()

        if task is not None:
            task.data = hoje
            task.save()
        else:
            TaskInformeDaily.insert(data=hoje).execute()


    def obter_por_data(self, data):
        try:
            return TaskInformeDaily.get(TaskInformeDaily.data == data)
            
        except TaskInformeDaily.DoesNotExist:
            return None

    def obter_hoje(self):
        try:
            return TaskInformeDaily.get(TaskInformeDaily.data == data.hoje())
            
        except TaskInformeDaily.DoesNotExist:
            return None

    def obter(self):
        try:
            return TaskInformeDaily.get()
        except TaskInformeDaily.DoesNotExist:
            return None