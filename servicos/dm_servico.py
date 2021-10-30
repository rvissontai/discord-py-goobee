from utilidades.parser_helper_util import CustomArgumentParser, string_para_args_parse
from servicos.goobee_teams_servico import goobee_teams_servico
from entidades.usuarios_model import Usuarios


class dm_servico():
    def __init__(self, bot):
        self.bot = bot
        self.servicos_disponiveis = ['goobe']
        self.goobee_service = goobee_teams_servico(bot)

    async def handle_private_message(self, message):
        parser = CustomArgumentParser(description='Registrar acesso.')

        parser.add_argument('-l', '--login', help='Login', required=True)
        parser.add_argument('-s', '--senha', help='Senha', required=True)

        try:
            args = message.content.split(' ')

            parse_args_result = parser.parse_args(args)

            if parser.error_message:
                await message.channel.send(parser.error_message)
                return

            await self.goobee_teste_autenticacao(message, parse_args_result)
        except SystemExit as e:
            await message.channel.send("Ocorreu um erro ao validar o comando.")


    async def goobee_teste_autenticacao(self, message, args):
        try:
            await message.channel.send("Vou confirmar no goobeteams se a suas credencias estão corretas, isso pode demorar alguns segundos...")

            encripted = await self.goobee_service.encriptar_autenticacao(args.login, args.senha)

            response = await self.goobee_service.autenticar(encripted["login"], encripted["password"])

            if(response.status_code == 200):
                try:
                    #Obter o usuário na base de dados, caso o usuário não exista, será gerada uma exceção;
                    Usuarios.get(Usuarios.idDiscord == message.author.id)

                    Usuarios.update(login = encripted["login"], senha = encripted["password"]).where(Usuarios.idDiscord == message.author.id).returning(Usuarios)
                except Usuarios.DoesNotExist:
                    Usuarios.insert(idDiscord=message.author.id, login=encripted["login"], senha=encripted["password"]).execute()
                
                await message.channel.send('Beleza, consegui logar aqui, agora é só ir no chat geral e mudar seu humor.')
            else:
                await message.channel.send('Não foi possível autenticar, tem certeza que me passou as informações certas?')
        except Exception as e:
            print(e)
            await message.channel.send('Vixi! ocorreu um problema interno, não vai rolar ):')