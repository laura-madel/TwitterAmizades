import os
import random

import requests
import json
import time

from dotenv import load_dotenv

load_dotenv(verbose=True)  # Throws error if no .env file is found

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# APAGAR QUANDO TIVER CONECTADO COM O BD
id_bd = []
name_bd = []
username_bd = []
bio_bd = []

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


def criar_url_infos_usuarie(users):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=" + users
    user_fields = "user.fields=name,username,protected,description,location,url,public_metrics,verified"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username and verified
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

def registra_no_bd(id, username, nome, bio = ""):

    #se já existe com o mesmo id no banco de dados
        #completa bio se não tiver
    #se não existe
        #adiciona as infos que tem

    id_bd.append(str(id))
    username_bd.append(str(username))
    name_bd.append(str(nome))
    bio_bd.append(str(bio))

def espera(segundos):
    while (segundos > 0):
        time.sleep(1)
        print(str(segundos))
        segundos = segundos - 1

def pesquisar_usuaries(users):
    url = criar_url_infos_usuarie(users)
    json_response = connect_to_endpoint(url)
    return json_response

def pesquisar_seguidores(seguide):

    url_base = criar_url_seguidores(seguide)
    url_pagina = url_base
    pagina = 1

    while(True):

        # Pesquisa e exibe os seguidores, 100 por vez
        json_response = connect_to_endpoint(url_pagina)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        print("--------------------------------------------------fim da pagina " + str(pagina) + "-----------------------------------------------------")

        # Guarda as infos dos seguidores no BD
        for item in json_response["data"]:
            registra_no_bd(item["id"],item["name"],item["username"])

        # Para o Twitter não bloquear, espera algum tempo aleatório
        espera(segundos=random.randint(100,600))

        # Atualiza o URL para a solicitação da próxima página de seguidores
        prox_pagina = json_response["meta"]["next_token"]
        url_pagina = url_base + "?pagination_token=" + prox_pagina