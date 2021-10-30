import os
import discord

from settings import *
from discord.ext import commands
from database import iniciar_database 
from servicos.dm_servico import dm_servico

bot = commands.Bot(command_prefix = ["?", "."], intents=discord.Intents().all())

iniciar_database()

@bot.event
async def on_ready():
    bot.load_extension("cogs.goobee_teams_cog")

    print('Bot goobee está pronto.')

    await bot.change_presence(activity=discord.Game(name="jogo da vida"))
    

@bot.event
async def on_message(message):
    print(str(message.author) + ' enviou uma mensagem')

    if message.author.bot:
        return

    private_message = message.author.dm_channel is not None and message.channel.id == message.author.dm_channel.id

    if private_message: 
        await dm_servico(bot).handle_private_message(message)
    else:
        await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Hummm, não conheço esse comando, na dúvida manda um .help pra ver os comandos')


bot.run(configuracao.obter_env('DISCORD-TOKEN'))