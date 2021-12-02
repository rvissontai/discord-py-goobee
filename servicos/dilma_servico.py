import random

class dilma_servico():
    def __init__(self):
        pass

    async def frase_aleatoria(self):
        frases = [u"Eu, para ir, eu faço uma escala. Para voltar, eu faço duas, para voltar para o Brasil. Neste caso agora nós tínhamos uma discussão. Eu tinha que sair de Zurique, podia ir para Boston, ou pra Boston, até porque... vocês vão perguntar, mas é mais longe? Não é não, a Terra é curva, viu?",
                        u"É interessante que muitas vezes no Brasil, você é, como diz o povo brasileiro, muitas vezes você é criticado por ter o cachorro e, outras vezes, por não ter o mesmo cachorro. Esta é uma crítica interessante que acontece no Brasil",
                        u"E nós criamos um programa que eu queria falar para vocês, que é o Ciência sem Fronteiras. Por que eu queria falar do Ciência sem Fronteiras para vocês? É que em todas as demais... porque nós vamos fazer agora o Ciência sem Fronteiras 2. O 1 é o 100 000, mas vai ter de continuar fazendo Ciência sem Fronteiras no Brasil",
                        u"Eu dou dinheiro pra minha filha. Eu dou dinheiro pra ela viajar, então é... é... Já vivi muito sem dinheiro, já vivi muito com dinheiro. -Jornalista: Coloca esse dinheiro na poupança que a senhora ganha R$10 mil por mês. -Dilma: O que que é R$10 mil?",
                        u"A única área que eu acho, que vai exigir muita atenção nossa, e aí eu já aventei a hipótese de até criar um ministério. É na área de... Na área... Eu diria assim, como uma espécie de analogia com o que acontece na área agrícola.",
                        u"Primeiro eu queria cumprimentar os internautas. -Oi Internautas! Depois dizer que o meio ambiente é sem dúvida nenhuma uma ameaça ao desenvolvimento sustentável. E isso significa que é uma ameaça pro futuro do nosso planeta e dos nossos países. O desemprego beira 20%, ou seja, 1 em cada 4 portugueses.",
                        u"Se hoje é o dia das crianças... Ontem eu disse: o dia da criança é o dia da mãe, dos pais, das professoras, mas também é o dia dos animais, sempre que você olha uma criança, há sempre uma figura oculta, que é um cachorro atrás. O que é algo muito importante!",
                        u"Todos as descrições das pessoas são sobre a humanidade do atendimento, a pessoa pega no pulso, examina, olha com carinho. Então eu acho que vai ter outra coisa, que os médicos cubanos trouxeram pro brasil, um alto grau de humanidade.",
                        u"No meu xinélo da humildade eu gostaria muito de ver o Neymar e o Ganso. Por que eu acho que.... 11 entre 10 brasileiros gostariam. Você veja, eu já vi, parei de ver. Voltei a ver, e acho que o Neymar e o Ganso têm essa capacidade de fazer a gente olhar.",
                        u"A população ela precisa da Zona Franca de Manaus, porque na Zona franca de Manaus, não é uma zona de exportação, é uma zona para o Brasil. Portanto ela tem um objetivo, ela evita o desmatamento, que é altamente lucravito. Derrubar arvores da natureza é muito lucrativo!",
                        u"Ai você fala o seguinte: \"- Mas vocês acabaram isso?\" Vou te falar: -\"Não, está em andamento!\" Tem obras que \"vai\" durar pra depois de 2010. Agora, por isso, nós já não desenhamos, não começamos a fazer projeto do que nós \"podêmo fazê\"? 11, 12, 13, 14... Por que é que não?"
                        u"Eu queria destacar uma questão, que é uma questão que está afetando o Brasil inteiro, que é a questão da vigilância sanitária: gente, é o vírus Aedes aegypti, com as suas diferentes modalidades: chikungunya, zika vírus.",
                        u"A presidente falava sobre a distribuição de recursos explorados do pré-sal. “Não é 30% dos recursos da exploração [do pré-sal]. É 30% de 25%. Ou 30%… de 30%. Portanto, não é 30%. Está entre 7,5% e um pouco mais, 12,5%. Não se trata de 30%"];

        return random.choice(frases)