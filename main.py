from get_users import *

if __name__ == '__main__':

    conexao = conectar_bd()

    arroba = "orionczar"

    pesquisar_seguidores(username_para_id(arroba), conexao)
    pesquisar_seguidos(username_para_id(arroba), conexao)

    desconectar_bd(conexao)