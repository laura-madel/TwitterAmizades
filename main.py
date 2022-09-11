from get_users import *

if __name__ == '__main__':
    conexao = conectar_bd()
    pesquisar_seguidores(username_para_id("orionczar"), conexao)
    print('pesquisa concluida!')
    desconectar_bd(conexao)
