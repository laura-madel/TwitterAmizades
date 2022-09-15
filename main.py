import sys
from get_users import *
from whatsapp_business_api import WhatsappAPI
from dotenv import load_dotenv

load_dotenv(verbose=True)  # Throws error if no .env file is found

whatsapp_1 = os.getenv("WHATSAPP_1")
whatsapp_2 = os.getenv("WHATSAPP_2")
id_numero_telefone = os.getenv("ID_NUMERO_TELEFONE")
token_acesso_zap = os.getenv("TOKEN_ACESSO_ZAP")

if __name__ == '__main__':

    # TODO cancelar outros processos desse codigo em python no servidor antes de recomeçar
    quantidade_seguir = 3
    quantidade_pesquisar = 3
    w = WhatsappAPI(phone_number_id=id_numero_telefone, access_token=token_acesso_zap)
    conexao = conectar_bd()
    # pesquisa_rotina("laura_madel_", conexao)
    alimentar_bd(melhores_para_pesquisar(quantidade_pesquisar, conexao), conexao)
    quem_seguir = melhores_para_pesquisar(quantidade_seguir, conexao)

    w.send_text_message(to=whatsapp_1, message='*Atenção para os @s de hoje:*')
    w.send_text_message(to=whatsapp_2, message='*Atenção para os @s de hoje:*')
    for i in range(0, quantidade_seguir, 1):
        mensagem = str(i + 1) + " - twitter.com/" + quem_seguir[i].username
        w.send_text_message(to=whatsapp_1, message=mensagem)
        w.send_text_message(to=whatsapp_2, message=mensagem)

    desconectar_bd(conexao)

    # TODO pra ver o resposta do chron no email
    sys.exit(0)