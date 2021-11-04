import discord

from discord.utils import get
from discord.ext import commands, tasks
from entidades.usuarios_model import Usuarios
from servicos.goobee_teams_servico import goobee_teams_servico
from comum.enum.enum_sentimento import sentimento
from comum.enum.enum_humor_response import humor_response
from comum.enum.enum_daily_response import daily_response
from utilidades.data import data, data_e_hora

class goobee_teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = goobee_teams_servico(self.bot)
        self.aviso_informe_humor.start()
        self.atualizar_backlog_presence.start()
        

    @tasks.loop(seconds=43200.0)
    async def atualizar_backlog_presence(self):
        backlog = await self.service.obter_backlog('449fa100-1e77-46da-a755-67a3519e5923')

        await self.bot.change_presence(activity=discord.Game(name="Backlog: " + backlog))


    @tasks.loop(seconds=300.0)
    async def aviso_informe_humor(self):
        print('Aviso Humor: Iniciando task...')

        if data_e_hora.agora().hour < 14:
            print('Aviso Humor: Ainda não são 14h...')
            return

        executou_hoje = await self.service.task_informe_humor_executou_hoje()

        if(executou_hoje):
            print('Aviso Humor: Task já executada...')
            return

        dia_da_semana = data.hoje().weekday()
        sexta_feira = 4

        if dia_da_semana > sexta_feira:
            print('Aviso Humor: É final de semana...')
            await self.service.task_informe_humor_adicionar()
            return
            
        print('Aviso Humor: Hora de executar, iniciando busca de usuários...')
        membros = []
        texto = ''
        usuarios = await self.service.obter_usuarios_que_nao_informaram_humor()

        print('Aviso Humor: Busca realizando, validando quantidae...')
        if usuarios is None or len(usuarios) == 0:
            await self.service.task_informe_humor_adicionar()
            return

        print('Aviso Humor: Encontar IDs dos usuários no Discord...')
        for user in usuarios:
            member = get(self.bot.get_all_members(), id=int(user.idDiscord))

            if member.desktop_status.value != 'offline' or member.mobile_status.value != 'offline':
                membros.append(member)
                texto += member.mention + ', '

        print('Aviso Humor: Procurando guilda Alcateia...')
        canal = await self.service.encontrar_canal('Alcateia')

        if canal is None:
            return

        print('Aviso Humor: Enviar mensagem na guilda...')
        if len(membros) > 1:
            await canal.send(texto + " como vocês estão se sentindo hoje?")
        elif len(membros) == 1:
            await canal.send(texto + " como está se sentindo hoje?")

        print('Aviso Humor: Definir aviso como endiado...')
        await self.service.task_informe_humor_adicionar()
    

    @commands.command(pass_context=True)
    async def login(self, ctx, arg):
        user = Usuarios.get(Usuarios.idDiscord == arg)
        response = await self.service.autenticar(user.login, user.senha)
        
        await ctx.send(str(response.text))


    @commands.command(pass_context=True)
    async def info(self, ctx, arg):
        user = Usuarios.get(Usuarios.idDiscord == arg)
        await ctx.send('Login: ' + str(user.login) + ' | Senha: ' + str(user.senha))

    @commands.command(pass_context=True, aliases=['f', 'F'])
    async def feliz(self, ctx):
        await self.add_humor(ctx, sentimento.feliz.value)

    @commands.command(pass_context=True, aliases=['b', 'B'] )
    async def bom(self, ctx):
        await self.add_humor(ctx, sentimento.bom.value)

    @commands.command(pass_context=True, aliases=['n', 'N'])
    async def nao_tao_bom(self, ctx):
        await self.add_humor(ctx, sentimento.nao_tao_bom.value)

    @commands.command(pass_context=True, aliases=['t', 'T'])
    async def triste(self, ctx):
        await self.add_humor(ctx, sentimento.triste.value)

    @commands.command(pass_context=True, aliases=['d', 'D'])
    async def daily(self, ctx):
        #Enviar uma mensagem para informar o usuário que o humor está sendo modificado.
        mensagem = await ctx.send('Definindo daily...')

        #Modificar daily como realizada
        response = await self.service.realizar_daily(ctx.author.id)

        #Definir a mensagem a ser exibida com base no response
        if(response == daily_response.sucesso):
            await mensagem.edit(content = 'Daily definida como realizada!')
            return
        
        if (response == daily_response.erro_realizar_daily):
            await mensagem.edit(content = 'Cara alguma coisa errada não ta certa, não consegui realizar a daily. ):')
            return
        
        if (response == daily_response.erro_autenticacao):
            await mensagem.edit(content = 'Cara deu alguma coisa errada com sua autenticação ):')
            return

        if (response == daily_response.erro_usuario_nao_existe):
            await mensagem.edit(content = 'Você ainda não me informou suas credenciais, enviei uma mensagem privada pra você, é só seguir as instruções por lá.')
            await ctx.author.send('Agora é só me falar seu email e senha em uma única mensagem beleza? fica tranquilo que não sou X9. \n ex: --login eu@email.com --senha senha123')     
            return


    async def add_humor(self, ctx, id_sentimento):
        #Enviar uma mensagem para informar o usuário que o humor está sendo modificado.
        mensagem = await ctx.send('Definindo humor...')

        #Modificar o humor do usuário
        response = await self.service.add_humor(ctx.author.id, id_sentimento)

        #Definir a mensagem a ser exibida com base no response
        if(response == humor_response.sucesso):
            await mensagem.edit(content = ctx.author.mention + ', seu humor foi alterado!')
            return
        
        if (response == humor_response.erro_alterar_humor):
            await mensagem.edit(content = format(ctx.author.mention) + ', alguma coisa errada não ta certa, não consegui alterar o humor ):')
            return
        
        if (response == humor_response.erro_autenticacao):
            await mensagem.edit(content = format(ctx.author.mention) + ', cara deu alguma coisa errada com sua autenticação ):')
            return

        if (response == humor_response.erro_usuario_nao_existe):
            await mensagem.edit(content = 'Você ainda não me informou suas credenciais, enviei uma mensagem privada pra você, é só seguir as instruções por lá.')
            await ctx.author.send('Agora é só me falar seu email e senha em uma única mensagem beleza? fica tranquilo que não sou X9. \n ex: --login eu@email.com --senha senha123')     
            return

        if (response == humor_response.timeout):
            await mensagem.edit(content = ctx.author.mention + ', a API do goobe não está respondendo, timeout ):')
            return


    @commands.command(pass_context=True)
    async def aviso(self, ctx):
        texto = await self.service.aviso_informe_humor()
        await ctx.send(texto)

def setup(bot):
    bot.add_cog(goobee_teams(bot))