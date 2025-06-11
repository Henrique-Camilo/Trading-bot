import configparser
import os
import re
import sqlite3
import time
from telethon import TelegramClient, events

# Caminho absoluto do config.ini
config_path = os.path.join(os.path.dirname(__file__), "config.ini")

# Carrega configuração
config = configparser.ConfigParser()
config.read(config_path)

if not config.sections():
    print("❌ ERRO: Não foi possível carregar o config.ini corretamente.")
    exit()

api_id = int(config["Telegram"]["API_ID"])
api_hash = config["Telegram"]["API_HASH"]
user_id = int(config["Telegram"]["USER_ID"])
phone_number = config["Telegram"]["PHONE_NUMBER"]  
saldo = float(config["Trading"]["SALDO_INICIAL"])  # Novo: Saldo inicial salvo no config.ini

# Nome da sessão com redundância
session_name = "sessao_segura"

# Declara `client` antes de usá-lo
client = TelegramClient(session_name, api_id, api_hash)

# Expressão regular para detectar sinais e seções
padrao_sinal = re.compile(r'(\d{1,2}) minutos de expiração (\S+): (\d{2}:\d{2}) (PUT|CALL)', re.IGNORECASE)
padrao_secao = re.compile(r'(PRIMÁRIO|GALE 1|GALE 2)', re.IGNORECASE)

# Variáveis para controle de mensagens processadas
ultimo_id_processado = 0
sinal_atual = None

@client.on(events.NewMessage(chats="SINAIS TRADER MÁGICO"))
async def captura_sinal(event):
    global ultimo_id_processado, sinal_atual, saldo

    # Ignora mensagens antigas
    if event.id <= ultimo_id_processado:
        return  
    ultimo_id_processado = event.id

    mensagem = event.message.message
    resultado_sinal = padrao_sinal.search(mensagem)
    resultado_secao = padrao_secao.search(mensagem)

    if resultado_sinal and resultado_secao:
        minutos = resultado_sinal.group(1)
        par = resultado_sinal.group(2)
        horario = resultado_sinal.group(3)
        direcao = resultado_sinal.group(4).upper()
        secao = resultado_secao.group(1).upper()

        # Atualiza saldo baseado na seção (exemplo: dedução de investimento)
        if secao == "PRIMÁRIO":
            saldo -= 10  # Valor fictício por operação
        elif secao == "GALE 1":
            saldo -= 20
        elif secao == "GALE 2":
            saldo -= 40

        # Registra o sinal atual
        sinal_atual = {
            "expiracao": minutos,
            "ativo": par,
            "horario": horario,
            "tipo": direcao,
            "secao": secao
        }

        texto = (
            f"🚀 *NOVO SINAL DETECTADO*\n"
            f"🕒 Expiração: {minutos} minutos\n"
            f"📉 Ativo: {par}\n"
            f"⏰ Horário: {horario}\n"
            f"📈 Direção: {direcao}\n"
            f"🔄 Seção: {secao}\n"
            f"💰 Saldo Atual: R${saldo:.2f}"
        )
        print(texto)
        await client.send_message(user_id, texto)

# Inicia o cliente
async def main():
    await client.start(phone_number)  
    print("🔎 Monitorando novos sinais no Telegram...")
    await client.run_until_disconnected()

import asyncio
asyncio.run(main())