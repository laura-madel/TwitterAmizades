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
    def __init__(self, id="", nome="", username="", bio=""):
        self.id = id
        self.nome = nome
        self.username = username
        self.bio = bio

# Recebe um vetor de (User) com username e retorna um vetor de (User) com mais informações
def pesquisa_por_usernames(users):

    if len(users) == 1:
        return pesquisa_por_username(users[0].username)

    usernames = []
    for user in users:
        usernames.append(user.username)
    url = "https://api.twitter.com/2/users/by?usernames=" + ','.join(usernames) + "&user.fields=name,username,description"
    json_response = connect_to_endpoint(url)

    users.clear()

    for user in json_response["data"]:
        users.append(User(id=str(user["id"]), nome=user["name"], username=user["username"], bio=user["description"]))

    return users

# Recebe SOMENTE UM username (String) e retorna um objeto (User) com mais informações
def pesquisa_por_username(username):
    url = "https://api.twitter.com/2/users/by?usernames=" + username + "&user.fields=name,username,description"
    json_response = connect_to_endpoint(url)
    user = json_response["data"][0]
    return User(id=str(user["id"]), nome=user["name"], username=user["username"], bio=user["description"])

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

def levantar_bios(users, conexao):
    return pesquisa_por_usernames(users)

def pesquisar_seguidores(seguide, conexao):

    url_base = criar_url_seguidores(seguide)
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
        users = levantar_bios(users, conexao)
        adiciona_user_bd(users, conexao)
        users.clear()

        # Atualiza o URL para a solicitação da próxima página de seguidores
        if 'next_token' in json_response["meta"]:
            prox_pagina = json_response["meta"]["next_token"]
            url_pagina = url_base + "?pagination_token=" + prox_pagina
        else:
            break

        # Para o Twitter não bloquear, espera um tempo aleatório
        espera(segundos=random.randint(2, 60))

        #! TODO: Continuar a partir da chave next_token