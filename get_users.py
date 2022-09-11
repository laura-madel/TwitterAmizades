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
    def __init__(self, id, nome="", username="", bio=""):
        self.id = id
        self.nome = nome
        self.username = username
        self.bio = bio

# Recebe uma string com o arroba e retorna uma string com o id (ou um vetor com os ids, se for mais de um)
def username_para_id(users):

    ids = []

    url = "https://api.twitter.com/2/users/by?usernames=" + users
    json_response = connect_to_endpoint(url)

    for user in json_response["data"]:
        ids.append(str(user["id"]))

    if len(ids) == 1:
        return ids[0]
    return ids


# Recebe uma string com o id e retorna um vetor de usuários (com id e bio)
def username_para_bio(usernames):

    users = []
    usernames = ','.join(usernames)

    url = "https://api.twitter.com/2/users/by?usernames=" + usernames + "&user.fields=id,username,description"
    json_response = connect_to_endpoint(url)

    for user in json_response["data"]:
        users.append(User(id=user["id"], username=user["username"], bio=user["description"]))

    if len(users) == 1:
        return users[0].bio
    return users


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

def registra_user_no_bd(conexao, id, username, nome, bio =""):
    adiciona_user_bd(conexao, str(id), str(username), str(nome), str(bio))

def espera(segundos):
    while (segundos > 0):
        time.sleep(1)
        print(str(segundos))
        segundos = segundos - 1

def pesquisar_usuaries(users):
    url = criar_url_infos_usuarie(users)
    json_response = connect_to_endpoint(url)
    return json_response

def levantar_bios(conexao, usernames):

    users = username_para_bio(usernames)

    for user in users:
        adiciona_bio_bd(conexao, user.id, user.bio)

def pesquisar_seguidores(conexao, seguide):

    url_base = criar_url_seguidores(seguide)
    url_pagina = url_base
    usernames = []

    while(True):

        # Pesquisa os seguidores, 100 por vez
        json_response = connect_to_endpoint(url_pagina)

        # print(json.dumps(json_response, indent=4, sort_keys=True))

        # Guarda as infos dos seguidores no BD
        for item in json_response["data"]:
            registra_user_no_bd(conexao, item["id"], item["name"], item["username"])
            usernames.append(item["username"])

        # Verifica se os users tem bio e coloca no BD
        levantar_bios(conexao, usernames)
        usernames.clear()

        # Para o Twitter não bloquear, espera um tempo aleatório
        espera(segundos=random.randint(2,60))

        # Atualiza o URL para a solicitação da próxima página de seguidores
        prox_pagina = json_response["meta"]["next_token"]
        url_pagina = url_base + "?pagination_token=" + prox_pagina
