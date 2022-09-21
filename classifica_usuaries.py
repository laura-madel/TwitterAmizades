from Usuarie import *

PONTOS_TRANS = 4
PONTOS_PRONOMES = 3
PONTOS_ARCO_IRIS = 2
PONTOS_ESTUDANTE = 2

QUANT_IDEAL_SEGUIDORES = 500
QUANT_IDEAL_SEGUIDES = 400

def pontua_bios(usuaries):

    pontuacoes = []
    interesses = [("⚧","trans","trava","travest",PONTOS_TRANS),
                  ("🌈",PONTOS_ARCO_IRIS),
                  ("ele","ela","elu","pronome",PONTOS_PRONOMES),
                  ("direito","⚖",PONTOS_ESTUDANTE),
                  ("UFPR","estud",PONTOS_ESTUDANTE)]

    for usuarie in usuaries:

        pontos = 0

        for interesse in interesses:
            i = 0
            while i < len(interesse) - 1:
                #TODO: RegEx Module
                if interesse[i] in usuarie.bio or interesse[i] in usuarie.nome or interesse[i] in usuarie.local:
                    pontos += interesse[-1]
                i += 1

        pontuacoes.append(Pontuacao(usuarie, pontos=pontos))
    usuaries.clear()
    pontuacoes.sort(reverse=True)

    return pontuacoes

# separar Direitos humanos / genero / nb / não binária/e/o

# 👿 fandom / otako; bookstan; multifandom