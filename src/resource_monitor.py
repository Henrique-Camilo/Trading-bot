import psutil
import time
import requests

# Configuração do Bot do Telegram
TELEGRAM_TOKEN = "7871363669:AAFlw5XIrf5nKOFdohzYKni0e62IPp_i1mI"
TELEGRAM_CHAT_ID = "1961302230"

# Função para enviar alertas no Telegram
def enviar_notificacao(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    requests.post(url, data=data)

# Função para monitorar recursos do sistema
def monitorar_recursos():
    uso_cpu = psutil.cpu_percent(interval=1)
    uso_ram = psutil.virtual_memory().percent

    print(f"🔍 CPU: {uso_cpu}% | RAM: {uso_ram}%")

    # Envia alerta se atingir limites críticos
    if uso_cpu > 80 or uso_ram > 90:
        mensagem_alerta = f"⚠️ ALERTA: Alto consumo detectado!\n🚀 CPU: {uso_cpu}% | RAM: {uso_ram}%"
        enviar_notificacao(mensagem_alerta)

# Loop de monitoramento contínuo
while True:
    monitorar_recursos()
    time.sleep(60)  # Verifica a cada 60 segundos