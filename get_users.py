import os
import random

import requests
import json
import time

from dotenv import load_dotenv
from db import *

load_dotenv(verbose=True)  # Throws error if no .env file is found

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

class User:
    def __init__(self, id="", nome="", username="", bio="", me_segue=False, eu_sigo=False, cont_seguidores=0,cont_seguidos=0):
        self.id = id
        self.nome = nome
        self.username = username
        self.bio = bio
        self.me_segue = me_segue
        self.eu_sigo = eu_sigo
        self.cont_seguidores = cont_seguidores
        self.cont_seguidos = cont_seguidos

# Recebe um vetor de (User) com username e retorna um vetor de (User) com mais informações
def pesquisa_por_usernames(users):

    if len(users) == 1:
        return pesquisa_por_username(users[0].username)

    usernames = []
    for user in users:
        usernames.append(user.username)

    url = "https://api.twitter.com/2/users/by?usernames=" + ','.join(usernames) + "&user.fields=name,username,description,public_metrics"
    json_response = connect_to_endpoint(url)

    users.clear()

    for user in json_response["data"]:

        id = str(user["id"])
        nome = user["name"]
        username = user["username"]
        bio = user["description"]
        cont_seguidores = user["public_metrics"]["following_count"]
        cont_seguidos = user["public_metrics"]["followers_count"]

        users.append(User(id=id, nome=nome, username=username, bio=bio, cont_seguidores=cont_seguidores, cont_seguidos=cont_seguidos))

    return users

# Recebe SOMENTE UM username (String) e retorna um objeto (User) com mais informações
def pesquisa_por_username(username):
    url = "https://api.twitter.com/2/users/by?usernames=" + username + "&user.fields=name,username,description,public_metrics"
    json_response = connect_to_endpoint(url)
    user = json_response["data"][0]

    id = str(user["id"])
    nome = user["name"]
    username = user["username"]
    bio = user["description"]
    cont_seguidores = user["public_metrics"]["following_count"]
    cont_seguidos = user["public_metrics"]["followers_count"]

    return User(id=id, nome=nome, username=username, bio=bio, cont_seguidores=cont_seguidores, cont_seguidos=cont_seguidos)

# Recebe o arroba e retorna o(s) id(s)
def username_para_id(username):
    return pesquisa_por_username(username).id

def criar_url_infos_usuarie(users):
    usernames = "usernames=" + users
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username and verified
    user_fields = "user.fields=name,username,protected,description,location,url,public_metrics,verified"
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url

def criar_url_seguidores(user_id):
    return "https://api.twitter.com/2/users/{}/followers".format(user_id)

def criar_url_seguides(user_id):
    return "https://api.twitter.com/2/users/{}/following".format(user_id)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

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

def pesquisar_usuaries(users):
    url = criar_url_infos_usuarie(users)
    json_response = connect_to_endpoint(url)
    return json_response

def adiciona_tags(users, tag):
    if tag == "marcar_como_seguido":
        for user in users:
            user.eu_sigo = True
    if tag == "marcar_como_seguidor":
        for user in users:
            user.me_segue = True

# def levantar_bios(users, conexao):
#     return pesquisa_por_usernames(users)

def pesquisar_com_paginas(user_id, url_base, conexao, tag = ""):
    url_pagina = url_base
    users = []

    while True:

        # Pesquisa os seguidores, 100 por vez
        json_response = connect_to_endpoint(url_pagina)

        # print(json.dumps(json_response, indent=4, sort_keys=True))

        # Guarda as infos dos seguidores no vetor do tipo (User)
        for item in json_response["data"]:
            user = User(id=item["id"], nome=item["name"], username=item["username"])
            users.append(user)

        # Verifica se ês usuaries tem bio e coloca no BD, todes ês 100 de uma vez
        users = pesquisa_por_usernames(users)
        ## TODO: juntar essas duas funções
        users = adiciona_tags(users, tag)
        adiciona_user_bd(users, conexao)
        users.clear()

        # Atualiza o URL para a solicitação da próxima página de seguidores
        if 'next_token' in json_response["meta"]:
            prox_pagina = json_response["meta"]["next_token"]
            url_pagina = url_base + "?pagination_token=" + prox_pagina
        else:
            break

        # Para o Twitter não bloquear, espera um tempo aleatório
        espera(segundos=random.randint(60*5, 60*6))

        #! TODO: interromper sem erro quando acaba https://developer.twitter.com/en/docs/twitter-api/rate-limits
        # Exception: Request returned an error: 429 {"title":"Too Many Requests","detail":"Too Many Requests","type":"about:blank","status":429}
        #! TODO: Continuar a partir da chave next_token
        #
        #! TODO: Implementar pesquisar_seguidos() também, generalizar essa função

def pesquisar_seguidores(id, conexao):
    pesquisar_com_paginas(id, criar_url_seguidores(id), conexao, tag="marcar_como_seguidor")
    print('pesquisa por seguidores concluida!')
def pesquisar_seguidos(id, conexao):
    pesquisar_com_paginas(id, criar_url_seguides(id), conexao, tag="marcar_como_seguido")
    print('pesquisa por seguidos concluida!')
