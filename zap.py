import os
from whatsapp_business_api import WhatsappAPI
from dotenv import load_dotenv

load_dotenv(verbose=True)  # Throws error if no .env file is found

whatsapp_1 = os.getenv("WHATSAPP_1")
whatsapp_2 = os.getenv("WHATSAPP_2")
id_numero_telefone = os.getenv("ID_NUMERO_TELEFONE")
token_acesso_zap = os.getenv("TOKEN_ACESSO_ZAP")
def conectar_zap():
    return WhatsappAPI(phone_number_id=id_numero_telefone, access_token=token_acesso_zap)
    print("Zap conectado!")

def enviar_zap(mensagem, zap):
        zap.send_text_message(to=whatsapp_1, message=mensagem)
        zap.send_text_message(to=whatsapp_2, message=mensagem)
