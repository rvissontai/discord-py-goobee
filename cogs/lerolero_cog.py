from discord.ext import commands

from servicos.lerolero_servico import lerolero_servico

class lerolero_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = lerolero_servico()

    @commands.command(pass_context=True)
    async def lero(self, ctx):
        frase_aleatoria = await self.service.frase_aleatoria();
        await ctx.send(frase_aleatoria)

def setup(bot):
    bot.add_cog(lerolero_cog(bot))