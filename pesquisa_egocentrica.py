import json
from twitter import *
def adiciona_tags(usuaries, tag):

    if tag == "seguide":
        for usuarie in usuaries:
            usuarie.eu_sigo = True

    if tag == "seguidor":
        for usuarie in usuaries:
            usuarie.me_segue = True

    return usuaries

def pesquisar_uma_pagina(conexao, tag):

    usuaries: list[Usuarie] = []

    if tag == "seguidor":
        url = criar_url_meus_seguidores()
    else:
        url = criar_url_meus_seguides()

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
    elif "errors" in json_response:
        return False
    return True

def minha_atualizacao_rotina(conexao):
    sucesso = pesquisar_uma_pagina(conexao, tag="seguidor")
    if sucesso:
        print('atualização de seguidores concluida!')
        espera()
        sucesso = pesquisar_uma_pagina(conexao, tag="seguide")
        if sucesso:
            print('atualização de seguides concluida!')
    else:
        print('Erro na atualização egocêntrica')
    espera()
