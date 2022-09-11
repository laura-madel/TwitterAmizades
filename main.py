from get_users import *

if __name__ == '__main__':

    conexao = conectar_bd()
    while True:
        pesquisa_rotina("laura_madel_", conexao)
        melhores_para_seguir(36, conexao)
        alimentar_bd(melhores_para_pesquisar(2, conexao))

    desconectar_bd(conexao)