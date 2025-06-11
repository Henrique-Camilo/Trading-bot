# src/bot.py

from telegram import Bot
from config import TOKEN, CHAT_ID

bot = Bot(token=TOKEN)

def enviar_mensagem(texto):
    """ Envia mensagens para o Telegram """
    bot.send_message(chat_id=CHAT_ID, text=texto)

if __name__ == "__main__":
    enviar_mensagem("✅ Bot iniciado com sucesso!")