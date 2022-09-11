from User import *

PONTOS_CARACTERE_TRANS = 4
PONTOS_PRONOMES = 2
PONTOS_ARCO_IRIS = 1
QUANT_IDEAL_SEGUIDORES = 500
QUANT_IDEAL_SEGUIDOS = 400

class Pontuacao:
    def __init__(self, user:User, pontos=0, incoerencia = 0):
        self.user = user
        self.pontos = pontos
        self.incoerencia = incoerencia

def pontua_bios(users):

    pontuacoes = []

    for user in users:

        pontos = 0
        incoerencia = 0

        pontos += verifica_caractere_trans(user.bio, user.nome)
        pontos += verifica_bandeira_lgbt(user.bio, user.nome)
        pontos += verifica_pronomes(user.bio)

        incoerencia += verifica_proporcao_seguidores(user.cont_seguidos, user.cont_seguidores)
        incoerencia += verifica_quantidade_seguidores(user.cont_seguidores)
        incoerencia += verifica_quantidade_seguidos(user.cont_seguidos)

        pontuacoes.append(Pontuacao(user, pontos=pontos, incoerencia=incoerencia))

    return pontuacoes

def verifica_caractere_trans(bio, nome):
    if "⚧" in bio or "⚧" in nome:
        return PONTOS_CARACTERE_TRANS
    return 0

def verifica_bandeira_lgbt(bio, nome):
    if "🌈" in bio or "🌈" in nome:
        return PONTOS_ARCO_IRIS
    return 0

def verifica_pronomes(bio):
    if "ele" in bio or "ela" in bio or "elu" in bio or "pronome" in bio:
        return PONTOS_PRONOMES
    return 0

#  DIREITO / UFPR / TRANS / TRAVA / TRAVESTI / PORN / +18 / NSFW

# Quanto maior esse índice maior a diferença entre seguidos e seguidores
def verifica_proporcao_seguidores(elu_segue, elu_eh_seguide):
    return abs(elu_segue - elu_eh_seguide) / 250.0

# Quanto maior mais longe do ideal
def verifica_quantidade_seguidores(elu_eh_seguide):
    return abs(elu_eh_seguide - QUANT_IDEAL_SEGUIDORES) / 100.0

# Quanto maior mais longe do ideal
def verifica_quantidade_seguidos(elu_segue):
    return abs(elu_segue - QUANT_IDEAL_SEGUIDOS) / 100.0