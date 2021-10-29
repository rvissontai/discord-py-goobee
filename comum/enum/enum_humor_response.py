from enum import Enum

class humor_response(Enum):
    sucesso = 1
    erro_alterar_humor = 2
    erro_autenticacao = 3
    erro_usuario_nao_existe = 4,
    timeout = 5