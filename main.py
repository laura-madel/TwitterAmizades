from get_users import *

if __name__ == '__main__':

    conexao = conectar_bd()
    baixa_user_bd(conexao)
    # pesquisa_rotina("fafuxa1", conexao)

    desconectar_bd(conexao)