import sys
from get_users import *
from zap import *

MEU_ARROBA = "laura_madel_"

if __name__ == '__main__':

    # TODO descobrir como fazer um log acessivel
    # TODO tempo entre uma pesquisa e outra e entre seguidos/seguidores!
    quantidade_seguir = 3
    quantidade_pesquisar = 3
    conexao = conectar_bd()
    zap = conectar_zap()
    # TODO Só precisa ver os seguidos, não precisa ser de rotina
    # pesquisa_rotina(MEU_ARROBA, conexao)
    # alimentar_bd(melhores_para_pesquisar(quantidade_pesquisar, conexao), conexao)
    quem_seguir = melhores_para_pesquisar(quantidade_seguir, conexao)
    enviar_zap(zap, "💖 *Atenção para os arrobas de hoje* 💖")
    for i in range(0, quantidade_seguir, 1):
        mensagem = "*" + str(i + 1) + "* • twitter.com/" + quem_seguir[i].username
        enviar_zap(zap, mensagem)

    desconectar_bd(conexao)