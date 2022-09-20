import sys
from pesquisa import *

MEU_ARROBA = "laura_madel_"

# TODO botar acentos nas variáveis
if __name__ == '__main__':
    # TODO descobrir como fazer um log acessivel
    quantidade_pesquisar = 1

    conexao_bd = conectar_bd()

    # TODO Só precisa ver os últimos seguidos, não precisa ver todas as páginas
    atualizar_seguides(Usuarie(id="1279200119129341952"), conexao_bd)

    # TODO: mandar zap quando terminar de pesquisar ume usuarie
    while True:
        alimentar_bd(melhores_para_pesquisar(quantidade_pesquisar, conexao_bd), conexao_bd)

    desconectar_bd(conexao_bd)
