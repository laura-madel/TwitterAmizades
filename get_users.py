import logging
import os
import random

import requests
import json
import time

from dotenv import load_dotenv
from classificacao_users import *
from db import *

load_dotenv(verbose=True)  # Throws error if no .env file is found

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

MEU_ID = "1279200119129341952"
TEMPO_MIN = 60*5
TEMPO_MAX = 60*6

def infos_de_interesse():
    return "name,username,description,public_metrics,profile_image_url,protected"
    #     # User fields are adjustable, options include:
    #     # created_at, description, entities, id, location, name,
    #     # pinned_tweet_id, profile_image_url, protected,
    #     # public_metrics, url, username and verified

def cria_url_username(username):
    return "https://api.twitter.com/2/users/by?usernames=" + username + "&user.fields=" + infos_de_interesse()

def cria_url_usernames(users):
    # TODO: não é possível que esse seja o melhor jeito!
    usernames = []
    for user in users:
        usernames.append(user.username)
    return "https://api.twitter.com/2/users/by?usernames=" + ','.join(usernames) + "&user.fields=" + infos_de_interesse()

def criar_url_seguidores(user_id):
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)

def criar_url_seguides(user_id):
    return "https://api.twitter.com/2/users/{}/following".format(user_id)

# Recebe o arroba e retorna o(s) id(s)
def username_para_id(username):
    return levanta_infos_user(username).id

# Recebe um vetor de (User) com username e retorna um vetor de (User) com mais informações
def levanta_infos_users(users):

    if len(users) == 1:
        return levanta_infos_user(users[0].username)


    url = cria_url_usernames(users)
    json_response = connect_to_endpoint(url)

    users.clear()

    for user in json_response["data"]:

        id = str(user["id"])
        nome = user["name"]
        username = user["username"]
        bio = user["description"]
        cont_seguidores = user["public_metrics"]["following_count"]
        cont_seguidos = user["public_metrics"]["followers_count"]
        foto = user["profile_image_url"]
        protegido = user["protected"]

        users.append(User(id=id, nome=nome, username=username, bio=bio, cont_seguidores=cont_seguidores, cont_seguidos=cont_seguidos, foto=foto, protegido=protegido))

    return users

# Recebe SOMENTE UM username (String) e retorna um objeto (User) com mais informações
def levanta_infos_user(username):
    url = cria_url_username(username)
    json_response = connect_to_endpoint(url)
    user = json_response["data"][0]

    id = str(user["id"])
    nome = user["name"]
    username = user["username"]
    bio = user["description"]
    cont_seguidores = user["public_metrics"]["following_count"]
    cont_seguidos = user["public_metrics"]["followers_count"]
    foto = user["profile_image_url"]
    protegido = user["protected"]

    return User(id=id, nome=nome, username=username, bio=bio, cont_seguidores=cont_seguidores, cont_seguidos=cont_seguidos, foto=foto, protegido=protegido)

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def espera(segundos):
    while segundos > 0:
        time.sleep(1)
        print(str(segundos))
        segundos = segundos - 1

def adiciona_tags(users, tag):
    if tag == "marcar_como_seguido":
        for user in users:
            user.eu_sigo = True
    if tag == "marcar_como_seguidor":
        for user in users:
            user.me_segue = True
    return users

def pesquisar_pagina(url, conexao, token="", tag=""):

    users: list[User] = []

    if token != "":
        url = url + "?pagination_token=" + token

    # Pesquisa os seguidores, 100 por vez
    json_response = connect_to_endpoint(url)

    print(json.dumps(json_response, indent=4, sort_keys=True))

# for item in json_response["data"]:
#
# KeyError: 'data'
# {
# "errors": [
#     {
#         "detail": "Sorry, you are not authorized to see the user with id: [1500850517966311430].",
#         "parameter": "id",
#         "resource_id": "1500850517966311430",
#         "resource_type": "user",
#         "section": "data",
#         "title": "Authorization Error",
#         "type": "https://api.twitter.com/2/problems/not-authorized-for-resource",
#         "value": "1500850517966311430"
#     }
# ]
# } ERRO QUANDO O USER É PROTEGIDO! mesmo que eu já siga
    if 'data' in json_response:
        # Guarda as infos dos seguidores no vetor do tipo (User)
        for item in json_response["data"]:
            user = User(id=item["id"], nome=item["name"], username=item["username"])
            users.append(user)

        # Verifica se ês usuaries tem bio e coloca no BD, todes ês 100 de uma vez
        users = levanta_infos_users(users)
        users = adiciona_tags(users, tag)
        adiciona_user_bd(users, conexao)

        users.clear()
        # Atualiza o URL para a solicitação da próxima página de seguidores
        if 'next_token' in json_response["meta"]:
            return json_response["meta"]["next_token"]
    return ""

def pesquisar_com_paginas(url_base, conexao, token = "", tag = ""):

    while True:
        token = pesquisar_pagina(url_base, conexao, token, tag)
        # TODO: indicar quanto falta pra terminar a pesquisa com o user, em %.
        logging.info("token: ", token)
        if token == "":
            break
        ##TODO: O primeiro tá pulando o tempo de espera??
        # Para o Twitter não bloquear, espera um tempo aleatório
        espera(segundos=random.randint(TEMPO_MIN, TEMPO_MAX))

        #! TODO: interromper sem erro quando acaba https://developer.twitter.com/en/docs/twitter-api/rate-limits e mandar mensagem de erro no zap
        # Exception: Request returned an error: 429 {"title":"Too Many Requests","detail":"Too Many Requests","type":"about:blank","status":429}

def pesquisar_seguidores(id, conexao):
    if id == MEU_ID:
        tag = "marcar_como_seguidor"
    else:
        tag = ""
    pesquisar_com_paginas(criar_url_seguidores(id), conexao, tag=tag)
    logging.info('pesquisa por seguidores concluida!')
def pesquisar_seguidos(id, conexao):
    tag = ""
    if id == MEU_ID:
        tag = "marcar_como_seguido"
    pesquisar_com_paginas(criar_url_seguides(id), conexao, tag=tag)
    logging.info('pesquisa por seguidos concluida!')

def pesquisar_seguidores_com_token(id, token, conexao):
    if id == MEU_ID:
        tag = "marcar_como_seguidor"
    else:
        tag = ""
    pesquisar_com_paginas(criar_url_seguidores(id), conexao, token=token, tag=tag)
    logging.info('pesquisa por seguidores com token concluida!')

def pesquisar_seguidos_com_token(id, token, conexao):
    tag = ""
    if id == MEU_ID:
        tag = "marcar_como_seguido"
    pesquisar_com_paginas(criar_url_seguides(id), conexao, token=token, tag=tag)
    logging.info('pesquisa por seguidos com token concluida!')
def pesquisa_rotina(arroba, conexao):
    pesquisar_seguidores(username_para_id(arroba), conexao)
    espera(segundos=random.randint(TEMPO_MIN, TEMPO_MAX))
    pesquisar_seguidos(username_para_id(arroba), conexao)

def alimentar_bd(users, conexao):
    for user in users:
        print("pesquisando ", user.username)
        pesquisa_rotina(user.username, conexao)
        adiciona_pesquisade(user, conexao)
        print(user.username, "pesquisade!")

def melhores_para_pesquisar(quantidade, conexao):

    users = baixa_user_bd(conexao)
    pesquisades = baixa_pesquisades(conexao)
    pontuacoes = pontua_bios(users)
    pontuacoes = filtra_relevantes_para_pesquisar(pontuacoes, pesquisades)
    users.clear()
    for i in range(0, quantidade, 1):
        users.append(pontuacoes[i].user)
    pontuacoes.clear()
    return users
def melhores_para_seguir(quantidade, conexao):
    users = baixa_user_bd(conexao)
    pontuacoes = pontua_bios(users)
    pontuacoes = filtra_relevantes(pontuacoes,pontuacao_min=10,filtro_porn=True,coerencia_min=0.0)
    for i in range(0, quantidade, 1):

        logging.info(i+1, "https://www.twitter.com/" + pontuacoes[i].user.username)
    # Descobrir como mandar por email.