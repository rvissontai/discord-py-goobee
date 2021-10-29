from discord.ext.commands.core import guild_only

import discord 
import argparse
import base64

class CustomArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(CustomArgumentParser, self).__init__(*args, **kwargs)

        self.error_message = ''

    def error(self, message):
        self.error_message = message

    def parse_args(self, *args, **kwargs):
        # catch SystemExit exception to prevent closing the application
        result = None
        try:
            result = super().parse_args(*args, **kwargs)
        except SystemExit:
            pass
        return result

def string_para_args_parse(*args):
    comandos = []

    for arg in args:  
        comandos.append(arg)

    if len(comandos) % 2 != 0:
        return;

    response = []

    index = 0

    while index < len(comandos):
        response.append(comandos[index] + ' ' + comandos[index+1])
        index+=2

    return response

def string_para_base64(texto):
    sample_string_bytes = texto.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    
    return base64_bytes.decode("ascii")

def encontrar_canal_padrao(bot, guild_nome):
    guild = discord.utils.get(bot.guilds, name=guild_nome)
    canal = discord.utils.get(guild.text_channels, name="amoux")

    if(canal is not None):
        return canal
    else:
        geral = discord.utils.get(guild.text_channels, name="geral")

        if geral is not None:
            return geral
        
    return None

        