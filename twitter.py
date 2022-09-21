import os
import requests
import random
import time

from dotenv import load_dotenv
load_dotenv(verbose=True)  # Throws error if no .env file is found
from db import *

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
meu_id_twitter = os.getenv("MEU_ID_TWITTER")

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

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r

# TODO: esse erro está parando o código! sem aviso = sem erro kkkkkjjjjjj
def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    if response.status_code != 200:
        espera()
        connect_to_endpoint(url)
        # raise Exception(
        #     "Request returned an error: {} {}".format(
        #         response.status_code, response.text
        #     )
        # )
        #! TODO: interromper sem erro quando acaba https://developer.twitter.com/en/docs/twitter-api/rate-limits e mandar mensagem de erro no zap
        # Exception: Request returned an error: 429 {"title":"Too Many Requests","detail":"Too Many Requests","type":"about:blank","status":429}
    return response.json()

def infos_de_interesse():
    return "name,username,description,public_metrics,profile_image_url,protected,location,url,verified"
    #     # User fields are adjustable, options include:
    #     # created_at, description, entities, id, location, name,
    #     # pinned_tweet_id, profile_image_url, protected,
    #     # public_metrics, url, username and verified

def junta_arrobas(usuaries):
    arrobas = []
    for usuarie in usuaries:
        arrobas.append(usuarie.arroba)
    return ','.join(arrobas)

def cria_url_arrobas(usuaries):
    return "https://api.twitter.com/2/users/by?usernames=" + junta_arrobas(usuaries) + "&user.fields=" + infos_de_interesse()

def criar_url_seguidores(usuarie):
    return "https://api.twitter.com/2/users/{}/followers".format(usuarie.id)

def criar_url_seguides(usuarie):
    return "https://api.twitter.com/2/users/{}/following".format(usuarie.id)

def criar_url_meus_seguidores():
    return "https://api.twitter.com/2/users/{}/followers".format(meu_id_twitter)

def criar_url_meus_seguides():
    return "https://api.twitter.com/2/users/{}/following".format(meu_id_twitter)

def unshorten_url(url):
    if url == "":
        return url
    else:
        try:
            url_aberta = requests.head(url, allow_redirects=True, timeout=2.5).url
        except:
            url_aberta = url
        finally:
            print("converti", url, "para", url_aberta)

    return url_aberta

def pega_local_json(usuarie_data):
    if "location" in usuarie_data:
        return usuarie_data["location"]
    return ""

# Recebe um vetor de (Usuarie) com arroba e retorna um vetor de (Usuarie) com mais informações
def levanta_infos_usuaries(usuaries):

    url = cria_url_arrobas(usuaries)
    json_response = connect_to_endpoint(url)

    usuaries.clear()

    for usuarie in json_response["data"]:

        id = str(usuarie["id"])
        nome = usuarie["name"]
        arroba = usuarie["username"]
        bio = usuarie["description"]
        cont_seguidores = usuarie["public_metrics"]["followers_count"]
        cont_seguides = usuarie["public_metrics"]["following_count"]
        foto = usuarie["profile_image_url"]
        protegide = usuarie["protected"]
        verificade = usuarie["verified"]
        local = pega_local_json(usuarie)
        url = unshorten_url(usuarie["url"])

        #TODO: esperar para ver se vai aparecer ume usuarie verificade
        usuaries.append(Usuarie(id=id, nome=nome, arroba=arroba, bio=bio, cont_seguidores=cont_seguidores, cont_seguides=cont_seguides, foto=foto, protegide=protegide, local=local, url=url, verificade=verificade))

    return usuaries