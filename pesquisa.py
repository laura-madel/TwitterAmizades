from classifica_usuaries import *
from pesquisa_db import *
from pesquisa_egocentrica import *

# Recebe ume usuárie com id e a conexão com o BD
def pesquisa_rotina(usuarie, conexao):
    sucesso = pesquisar(criar_url_seguidores(usuarie), conexao)
    if sucesso:
        print('pesquisa por seguidores concluida!')
        sucesso = pesquisar(criar_url_seguides(usuarie), conexao)
        if sucesso:
            print('pesquisa por seguides concluida!')
        else:
            print('Erro na pesquisa de seguides deste usuário')

    else:
        print('Erro na pesquisa de seguidores deste usuário')
    return sucesso

# TODO: continuar pesquisa de onde parou
# def pesquisar_seguidores_com_token(id, token, conexao):
#     pesquisar_com_paginas(criar_url_seguidores(id), conexao, token=token)
#     logging.info('pesquisa por seguidores com token concluida!')
#
# def pesquisar_seguides_com_token(id, token, conexao):
#     pesquisar_com_paginas(criar_url_seguides(id), conexao, token=token)
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
    usuaries_aux = []
    pesquisades = baixa_pesquisades(conexao)
    #TODO: pesquisar for pesquisade in pesquisades para não ter q passar por todes es usuaries
    #TODO: usar remove() e abandonar o usuaries_aux
    for usuarie in usuaries:
        # TODO: remover perfis fechados
        # TODO: pesquisar só pessoas trans
        if usuarie.id not in pesquisades:
            usuaries_aux.append(usuarie)
    pontuacoes = pontua_bios(usuaries_aux)
    del usuaries_aux
    usuaries.clear()
    for i in range(0, quantidade, 1):
        if i < len(pontuacoes):
            usuaries.append(pontuacoes[i].usuarie)
            print("será pesquisade:", pontuacoes[i].usuarie.arroba, pontuacoes[i].usuarie.nome, pontuacoes[i].pontos)
        else:
            print("poucos usuários aptos no BD")
    # TODO: transformar todos os clear() em del quando fizer sentido
    del pontuacoes
    del pesquisades
    return usuaries

def pesquisar(url, conexao):

    usuaries: list[Usuarie] = []
    url_base = url
    while True:

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
            adiciona_usuarie_bd(usuaries, conexao)

            usuaries.clear()

            # Para o Twitter não bloquear, espera um tempo aleatório
            espera()

            # Atualiza o URL para a solicitação da próxima página de seguidores
            if 'next_token' in json_response["meta"]:
                url = url_base + "?pagination_token=" + json_response["meta"]["next_token"]
            # Não tem próxima página, é a última.
            else:
                return True
        elif "errors" in json_response:
            return False