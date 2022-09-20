from Usuarie import *

PONTOS_TRANS = 8
PONTOS_PRONOMES = 4
PONTOS_ARCO_IRIS = 2
PONTOS_ESTUDANTE = 1

QUANT_IDEAL_SEGUIDORES = 500
QUANT_IDEAL_SEGUIDES = 400
def pontua_bios(usuaries):

    pontuacoes = []

    for usuarie in usuaries:

        pontos = 0
        incoerencia = 0

        pontos += verifica_trans(usuarie.bio, usuarie.nome)
        pontos += verifica_lgbt(usuarie.bio, usuarie.nome)
        pontos += verifica_pronomes(usuarie.bio)
        pontos += verifica_estudante(usuarie.bio, usuarie.nome)
        # Se a quantidade de seguidoras for pequena (mais perto do ou menor do que ideal), a proporção só importa se não seguir ninguém
        incoerencia += verifica_proporcao_seguidores(usuarie.cont_seguides, usuarie.cont_seguidores)
        incoerencia += verifica_quantidade_seguidores(usuarie.cont_seguidores)
        incoerencia += verifica_quantidade_seguides(usuarie.cont_seguides)

        # Deixa a incoerencia no intervalo [0,1]
        if incoerencia < 10.0:
            incoerencia = incoerencia/10.0
        else:
            incoerencia = 1

        coerencia = 1.0 - incoerencia

        porn = verifica_porn(usuarie.bio, usuarie.nome)

        pontuacoes.append(Pontuacao(usuarie, pontos=pontos, coerencia=coerencia, porn=porn))

    usuaries.clear()
    pontuacoes.sort(reverse=True)

    return pontuacoes

# TODO: coerencia importa? remover
# TODO: pesquisar só pessoas trans
def filtra_relevantes_para_pesquisar(pontuacoes, pesquisades, pontuacao_min=0,filtro_porn=True,coerencia_min=0.0):
    pontuacoes_filtradas = []
    for pontuacao in pontuacoes:
        if pontuacao.pontos >= pontuacao_min and pontuacao.porn != filtro_porn and pontuacao.coerencia >= coerencia_min and pontuacao.usuarie.id not in pesquisades:
            pontuacoes_filtradas.append(pontuacao)
    pontuacoes.clear()
    pontuacoes_filtradas.sort(reverse=True)
    return pontuacoes_filtradas

def verifica_trans(bio, nome):
    if "⚧" in bio or "⚧" in nome or "trans" in bio or "trans" in nome or "trava" in bio or "trava" in nome or "travesti" in bio or "travesti" in nome:
        return PONTOS_TRANS
    return 0

def verifica_lgbt(bio, nome):
    if "🌈" in bio or "🌈" in nome:
        return PONTOS_ARCO_IRIS
    return 0

def verifica_pronomes(bio):
    if "ele" in bio or "ela" in bio or "elu" in bio or "pronome" in bio:
        return PONTOS_PRONOMES
    return 0

def verifica_estudante(bio, nome):
    if "direito" in bio or "direito" in nome or "UFPR" in bio or "UFPR" in nome or "⚖" in bio or "⚖" in nome or "estud" in bio or "estud" in nome:
        return PONTOS_ESTUDANTE
    return 0

# separar Direitos humanos / genero / nb / não binária/e/o

# 👿 fandom / otako; bookstan; multifandom

# 🔞 TODO: colocar uma etiqueta no verifica_porn para não excluir e enviar por zap com um aviso
def verifica_porn(bio, nome):
    if "porn" in bio or "porn" in nome or "+18" in bio or "+18" in nome or "NSFW" in bio or "NSFW" in nome:
        return True
    return False

# Quanto maior esse índice maior a diferença entre seguides e seguidores
def verifica_proporcao_seguidores(elu_segue : int, elu_eh_seguide : int):
    if elu_segue is not None and elu_eh_seguide is not None:
        diferença = abs(elu_segue - elu_eh_seguide)
    else:
        # TODO inverter a lógica para poder mandar 0 aqui
        diferença = 100
    return diferença / 100.0

# Quanto maior mais longe do ideal
def verifica_quantidade_seguidores(elu_eh_seguide):
    if elu_eh_seguide is not None:
        diferença = abs(elu_eh_seguide - QUANT_IDEAL_SEGUIDORES)
    else:
        diferença = 100
    return diferença / 100.0

# Quanto maior mais longe do ideal
def verifica_quantidade_seguides(elu_segue):
    if elu_segue is not None:
        diferença = abs(elu_segue - QUANT_IDEAL_SEGUIDES)
    else:
        diferença = 100
    return diferença / 100.0