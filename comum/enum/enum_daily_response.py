from enum import Enum

class daily_response(Enum):
    sucesso = 1
    erro_realizar_daily = 2
    erro_autenticacao = 3
    erro_usuario_nao_existe = 4