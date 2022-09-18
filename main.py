import sys
from get_users import *
from zap import *

MEU_ARROBA = "laura_madel_"

if __name__ == '__main__':
    # TODO descobrir como fazer um log acessivel
    # TODO tempo entre uma pesquisa e outra e entre seguidos/seguidores!
    quantidade_seguir = 25
    quantidade_pesquisar = 10

    conexao = conectar_bd()
    meu_zap = conectar_zap()

    # TODO Só precisa ver os últimos seguidos, não precisa ver todas as páginas
    # atualizar_seguides(MEU_ARROBA, conexao)

    # TODO: mandar zap quando terminar de pesquisar ume usuarie
    alimentar_bd(melhores_para_pesquisar(quantidade_pesquisar, conexao), conexao)

    # Envia os melhores para seguir para o meu zap
    quem_seguir = melhores_para_seguir(quantidade_seguir, conexao)
    mensagem = "💌 *Atenção para os arrobas de hoje* 💌\n\n"
    for i in range(0, quantidade_seguir, 1):
        mensagem += "*" + str(i + 1) + "* • twitter.com/" + quem_seguir[i].username + "\n"
    enviar_zap(mensagem, meu_zap)

    desconectar_bd(conexao)