import requests
import json
import os
from comum.enum.enum_verificar_daily_response import verificar_daily_response

from database import Usuarios
from discord.utils import get
from utilidades.data import data, data_e_hora
from utilidades.parser_helper_util import string_para_base64, encontrar_canal_padrao, base64_para_string

from comum.enum.enum_humor_response import humor_response
from comum.enum.enum_daily_response import daily_response

from repositorios.humor_diario_repositorio import humor_diario_repositorio
from repositorios.task_informe_humor_repositorio import task_informe_humor_repositorio
from repositorios.task_informe_daily_repositorio import task_informe_daily_repositorio
from repositorios.log_humor_repositorio import log_humor_repositorio

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class goobee_teams_servico():
    def __init__(self, bot):
        url = os.getenv('GOOBEE-URL')

        self.bot = bot
        self.url_auth = url + os.getenv('GOOBEE-ENDPOINT-AUTH')
        self.url_humor = url + os.getenv('GOOBEE-ENDPOINT-HUMOR')
        self.url_editar_humor = url + os.getenv('GOOBEE-ENDPOINT-EDITAR-HUMOR')
        self.url_daily = url + os.getenv('GOOBEE-ENDPOINT-DAILY')
        self.url_backlog = url + os.getenv('GOOBEE-ENDPOINT-BACKLOG-OBTER')
        self.humor_diario_repositorio = humor_diario_repositorio()
        self.task_informe_humor_repositorio = task_informe_humor_repositorio()
        self.task_informe_daily_repositorio = task_informe_daily_repositorio()
        self.log_humor_repositorio = log_humor_repositorio()


    async def autenticar(self, user, senha):
        return requests.post(self.url_auth, data=None, json={'usuario': user, 'senha': senha }, timeout=10)


    async def add_humor(self, idDiscord, id_sentimento):
        try:
            user = Usuarios.get(Usuarios.idDiscord == idDiscord)
            response = await self.teste_obter_token(user.login, user.senha)
            
            # if(response.status_code != 200 or response.ok is not True):
            #     return humor_response.erro_autenticacao
            
            # sucesso_response = json.loads(response.text)

            header = { 'Authorization': 'Bearer ' + response["token"] }

            sentimento_diario_response = await self.obter_sentimento_diario(response["token"], response["idPessoa"])

            if sentimento_diario_response is None:
                param = {
                    'idPessoa': response["idPessoa"],
                    'idResponsavelCriacao': response["id"],
                    'sentimento': id_sentimento
                }

                humorResponse = requests.post(self.url_humor, json=param, headers=header)
            else:
                param = {
                    'idSentimentoPessoa': sentimento_diario_response,
                    'idResponsavelCriacao': response["id"],
                    'sentimento': id_sentimento
                }

                humorResponse = requests.put(self.url_editar_humor + sentimento_diario_response, json=param, headers=header)

            if(humorResponse.status_code != 200 or humorResponse.ok is not True):
                return humor_response.erro_alterar_humor
                
            self.humor_diario_repositorio.adicionar(idDiscord=idDiscord)

            return humor_response.sucesso
        except Usuarios.DoesNotExist:
            return humor_response.erro_usuario_nao_existe

        except requests.exceptions.Timeout:
            return humor_response.timeout

        except Exception as e:
            print(e)
            return humor_response.erro_alterar_humor


    async def obter_sentimento_diario(self, token, id_pessoa):
        response = requests.get(
            os.getenv('GOOBEE-URL') + '/api/Home/InformaHumor', 
            params={'idPessoa': id_pessoa },
            headers= { 'Authorization': 'Bearer ' + token })

        if response.status_code != 200:
            return None

        model = json.loads(response.text)

        if model["idSentimentoPessoa"] is None:
            return None

        return model["idSentimentoPessoa"]


    async def realizar_daily(self, idDiscord):
        try:
            user = Usuarios.get(Usuarios.idDiscord == idDiscord)
            response = await self.autenticar(user.login, user.senha)
            
            if(response.status_code == 200):
                sucesso_response = json.loads(response.text)

                header = { 'Authorization': 'Bearer ' + sucesso_response["token"] }
                param = {
                    'dia': data_e_hora.agora().isoformat(),
                    'idTime': sucesso_response["idsTimes"][0],
                    'idResponsavelRegistro': sucesso_response["idPessoa"],
                    'observacao':''
                }

                response = requests.post(self.url_daily, json=param, headers=header)

                if(response.status_code == 200):
                    self.task_informe_daily_repositorio.adicionar()
                    return daily_response.sucesso

                return daily_response.erro_realizar_daily
            else:
                return daily_response.erro_autenticacao

        except Usuarios.DoesNotExist:
            return daily_response.erro_usuario_nao_existe
        except Exception as e:
            print(e)
            return daily_response.erro_realizar_daily


    async def verificar_daily(self):
        user = Usuarios.get(Usuarios.idDiscord == '765610511655108611')
        response = await self.autenticar(user.login, user.senha)

        if(response.status_code != 200):
            return { 'status': verificar_daily_response.erro_autenticacao, 'realizada': None }

        sucesso_response = json.loads(response.text)
        id_time = sucesso_response["idsTimes"][0]

        response = requests.get(
            os.getenv('GOOBEE-URL') + '/api/PraticaAgil/PegarConfiguracaoDaily/' + id_time, 
            params={},
            headers= { 'Authorization': 'Bearer ' + sucesso_response["token"] })

        if response.status_code != 200:
            return { 'status': verificar_daily_response.erro_verificar_daily, 'realizada': None }

        model = json.loads(response.text)

        if model["realizada"] is None:
            return None

        return { 'status': verificar_daily_response.sucesso, 'realizada': model["realizada"]}


    async def encriptar_autenticacao(self, login, password):
        return {
            "login": string_para_base64(login),
            "password": string_para_base64(password)
        };
        
    async def teste_obter_token(self, login, password):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"

        options = webdriver.ChromeOptions()
        options.headless = True

        if os.environ.get('GOOGLE_CHROME_BIN') is not None:
            options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-extensions")
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options, desired_capabilities=caps)

        driver.get('https://app.beefor.io/login')
        
        input_email = driver.find_element_by_css_selector("input[formcontrolname=\"email\"")
        input_senha = driver.find_element_by_css_selector("input[formcontrolname=\"senha\"")
        button_login = driver.find_element_by_css_selector("button[type=\"submit\"")

        input_email.send_keys(login)
        input_senha.send_keys(password)

        button_login.click()

        try:
            element_present = EC.presence_of_element_located((By.ID, 'focusNavigatorMenuPerfil'))
            WebDriverWait(driver, timeout=10).until(element_present)
        except TimeoutException:
            return False

        logs = driver.get_log("performance")

        try:
            return await self.process_browser_logs_for_network_events(logs, driver)
        except Exception as ex:
            print(ex)

        driver.quit()

    async def process_browser_logs_for_network_events(self, logs, driver):
        for entry in logs:
            log = json.loads(entry["message"])["message"]

            if log["method"] != "Network.responseReceived":
                continue

            if "params" not in log or "response" not in log["params"]:
                continue

            rep = log["params"]["response"]
            url = rep["url"]

            if url.endswith("Token") == False:
                continue

            try:
                response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': log["params"]["requestId"]})
                return json.loads(response_body["body"])
            except:
                pass

        return {}
        
    async def encontrar_canal(self, guild_nome):
        canal = encontrar_canal_padrao(self.bot, guild_nome)

        if canal is None:
            print("Nenhum canal padrão configurado")
            return

        return canal

        

    async def obter_usuarios_que_nao_informaram_humor(self):
        try:
            notificar_usuarios = []
            users = Usuarios.select().execute()
            
            for user in users:
                humor = self.humor_diario_repositorio.obter(user.idDiscord, data.hoje())

                if humor is None:
                    notificar_usuarios.append(user)

            return notificar_usuarios

        except Exception as e:
            print(e)        
            return None

    
    async def task_informe_humor_adicionar(self):
        self.task_informe_humor_repositorio.adicionar()

    
    async def task_informe_humor_executou_hoje(self):
        model = self.task_informe_humor_repositorio.obter_hoje()

        if model is None:
            return False

        return True

    async def aviso_informe_humor(self):
        membros = []
        texto = ''
        usuarios = await self.obter_usuarios_que_nao_informaram_humor()

        for user in usuarios:
            member = get(self.bot.get_all_members(), id=int(user.idDiscord))

            if member.desktop_status.value != 'offline' or member.mobile_status.value != 'offline':
                membros.append(member)
                #texto += member.mention + ', '
                texto += member.name + ', '

        return texto


    async def task_informe_daily_executou_hoje(self):
        model = self.task_informe_daily_repositorio.obter_hoje()

        if model is not None:
            return True

        response = await self.verificar_daily()

        if response["status"] != verificar_daily_response.sucesso:
            return

        return response["realizada"]


    async def task_informe_daily_adicionar(self):
        self.task_informe_daily_repositorio.adicionar()

    async def obter_backlog(self, id_time):
        user = Usuarios.get()
        response = await self.autenticar(user.login, user.senha)
            
        if(response.status_code == 200):
            sucesso_response = json.loads(response.text)

            header = { 'Authorization': 'Bearer ' + sucesso_response["token"] }
            response = requests.get(self.url_backlog + '/' + id_time, headers=header)

            if(response.status_code == 200):
                sucesso_response = json.loads(response.text)
                return sucesso_response["resultado"]