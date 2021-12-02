from discord.ext import commands

from servicos.dilma_servico import dilma_servico

class dilma_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = dilma_servico()

    @commands.command(pass_context=True)
    async def dilma(self, ctx):
        frase_aleatoria = await self.service.frase_aleatoria();
        await ctx.send(frase_aleatoria)

def setup(bot):
    bot.add_cog(dilma_cog(bot))