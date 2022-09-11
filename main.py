from get_users import *

if __name__ == '__main__':

    conexao = conectar_bd()

    alimentar_bd(melhores_para_pesquisar(3, conexao))
    pesquisa_rotina("laura_madel_", conexao)
    melhores_para_seguir(36, conexao)

    desconectar_bd(conexao)