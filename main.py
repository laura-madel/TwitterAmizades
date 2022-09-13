from get_users import *
#from whatsapp_business_api import WhatsappAPI

if __name__ == '__main__':

    conexao = conectar_bd()
    # cancelar outros processos desse codigo em python no servidor antes de recomeçar
    # melhores_para_seguir(36, conexao)
    # pesquisa_rotina("laura_madel_", conexao)
    while True:
        alimentar_bd(melhores_para_pesquisar(5, conexao), conexao)


    desconectar_bd(conexao)

    # phone_number_id = '103726292491399'
    # access_token = 'EAANAKWTSJaYBABZBV58JgPmmvZCcxLRZBW0LRAQkhD9Vw4NkPe0vYCqTB5K1la0KgkLoIOkdE4zcKGNXhRZB1Iaswz8E6JP21fBlhodL4oIXqJ9Ivl5xBBxtI9Xxlmnz7JNdt7l6MZA6rqdi1aSpdG4yIiZBOSWkdCSiJJTITtq1A8ZC05qaPuSWZAqZAZAGnt9zbcEvo0mtlPiAZDZD'
    #
    # w = WhatsappAPI(phone_number_id=phone_number_id, access_token=access_token)
    #
    # w.send_text_message(to='5541988779000', message='This is a test!')