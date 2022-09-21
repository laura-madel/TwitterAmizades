import sys
from pesquisa import *

MEU_ARROBA = "laura_madel_"
# marcar eu mesma como minha própria seguidora e seguida no bd
# TODO botar acentos nas variáveis
# TODO descobrir como fazer um log acessivel
if __name__ == '__main__':
    quantidade_pesquisar = 10

    conexao_bd = conectar_bd()

    # minha_atualizacao_rotina(conexao_bd)

    while True:
        alimentar_bd(melhores_para_pesquisar(quantidade_pesquisar, conexao_bd), conexao_bd)

    desconectar_bd(conexao_bd)
