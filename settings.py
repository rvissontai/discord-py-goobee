import os

from dotenv import load_dotenv

load_dotenv()

class configuracao:

    @staticmethod
    def obter_env(chave):
        return os.getenv(chave)
