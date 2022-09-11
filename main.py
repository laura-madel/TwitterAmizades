from get_users import *

if __name__ == '__main__':
    conexao = conectar_bd()
    pesquisar_seguidores(conexao, username_para_id("laura_madel_"))
    desconectar_bd(conexao)
    print('pesquisa concluida!')
