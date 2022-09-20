import logging
import json
import random
import time

from classifica_usuaries import *
from twitter import *
from pesquisa_db import *
from pesquisa_egocentrica import *

TEMPO_MIN_ESPERA = 270
TEMPO_MAX_ESPERA = 330

def espera():
    segundos = random.randint(TEMPO_MIN_ESPERA, TEMPO_MAX_ESPERA)
    while segundos > 0:
        time.sleep(1)
        if segundos % 2 == 0:
            print(str(segundos), "-----+")
        else:
            print(str(segundos))
        segundos = segundos - 1

def pesquisar_seguidores(usarie, conexao):
    if usarie.id == "1279200119129341952":
        tag = "marcar_como_seguidor"
    else:
        tag = ""
    sucesso = pesquisar_paginas(criar_url_seguidores(usarie), conexao, tag=tag)
    return sucesso

def pesquisar_seguides(usarie, conexao):
    if usarie.id == "1279200119129341952":
        tag = "marcar_como_seguide"
    else:
        tag = ""
    sucesso = pesquisar_paginas(criar_url_seguides(usarie), conexao, tag=tag)
    return sucesso

def atualizar_seguides(usuarie, conexao):
    pesquisar_seguides(usuarie, conexao)

# Recebe ume usuárie com id e a conexão com o BD
def pesquisa_rotina(usuarie, conexao):
    sucesso = pesquisar_seguidores(usuarie, conexao)
    if sucesso:
        print('pesquisa por seguidores concluida!')
        sucesso = pesquisar_seguides(usuarie, conexao)
        if sucesso:
            print('pesquisa por seguides concluida!')
        else:
            print('Erro na pesquisa de seguides deste usuário')

    else:
        print('Erro na pesquisa de seguidores deste usuário')
    return sucesso

# TODO: continuar pesquisa de onde parou
# def pesquisar_seguidores_com_token(id, token, conexao):
#     if id == MEU_ID:
#         tag = "marcar_como_seguidor"
#     else:
#         tag = ""
#     pesquisar_com_paginas(criar_url_seguidores(id), conexao, token=token, tag=tag)
#     logging.info('pesquisa por seguidores com token concluida!')
#
# def pesquisar_seguides_com_token(id, token, conexao):
#     tag = ""
#     if id == MEU_ID:
#         tag = "marcar_como_seguide"
#     pesquisar_com_paginas(criar_url_seguides(id), conexao, token=token, tag=tag)
#     logging.info('pesquisa por seguides com token concluida!')

# Recebe ume (Usuarie) com id e arroba + a conexão com o BD
def alimentar_bd(usuaries, conexao):
    for usuarie in usuaries:
        inicia_pesquisa_bd(usuarie, conexao)
        print("pesquisando ", usuarie.arroba)
        sucesso = pesquisa_rotina(usuarie, conexao)
        if sucesso:
            conclui_pesquisa_bd(usuarie, conexao)
        else:
            registra_erro_pesquisa_bd(usuarie, conexao)
            print("Usuárie < " + usuarie.arroba + " > com perfil fechado")
        print(usuarie.arroba, "pesquisade!")

def melhores_para_pesquisar(quantidade, conexao):

    usuaries = baixa_usuaries_bd(conexao)
    pesquisades = baixa_pesquisades(conexao)
    pontuacoes = pontua_bios(usuaries)
    pontuacoes = filtra_relevantes_para_pesquisar(pontuacoes, pesquisades)
    usuaries.clear()
    for i in range(0, quantidade, 1):
        usuaries.append(pontuacoes[i].usuarie)
    pontuacoes.clear()
    return usuaries

def pesquisar_uma_pagina(url, conexao, token="", tag=""):

    usuaries: list[Usuarie] = []

    if token != "":
        url = url + "?pagination_token=" + token

    # Pesquisa os seguidores, 100 por vez
    json_response = connect_to_endpoint(url)

    print(json.dumps(json_response, indent=4, sort_keys=True))

    if 'data' in json_response:
        # Guarda as infos dos seguidores no vetor do tipo (Usuarie)
        for item in json_response["data"]:
            usuarie = Usuarie(id=item["id"], nome=item["name"], arroba=item["username"])
            usuaries.append(usuarie)

        # Verifica se ês usuaries tem bio e coloca no BD, todes ês 100 de uma vez
        usuaries = levanta_infos_usuaries(usuaries)
        usuaries = adiciona_tags(usuaries, tag)
        adiciona_usuarie_bd(usuaries, conexao)

        usuaries.clear()

        # Para o Twitter não bloquear, espera um tempo aleatório
        espera()

        # Atualiza o URL para a solicitação da próxima página de seguidores
        if 'next_token' in json_response["meta"]:
            return json_response["meta"]["next_token"]
        #TODO : definitivamente não é a melhor forma
    elif "errors" in json_response:
        return "erro"
    return "fim"

# TODO: juntar essas duas funções
def pesquisar_paginas(url_base, conexao, token ="", tag =""):

    while True:
        token = pesquisar_uma_pagina(url_base, conexao, token, tag)
        # TODO: indicar quanto falta pra terminar a pesquisa com o usuarie, em %.

        if token == "fim":
            return True
        if token == "erro":
            return False

        #! TODO: interromper sem erro quando acaba https://developer.twitter.com/en/docs/twitter-api/rate-limits e mandar mensagem de erro no zap
        # Exception: Request returned an error: 429 {"title":"Too Many Requests","detail":"Too Many Requests","type":"about:blank","status":429}
