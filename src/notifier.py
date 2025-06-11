import requests

# Configuração do Bot do Telegram
TELEGRAM_TOKEN = "7871363669:AAFlw5XIrf5nKOFdohzYKni0e62IPp_i1mI"
TELEGRAM_CHAT_ID = "1961302230"

# Função para enviar notificações automáticas
def enviar_notificacao(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    
    resposta = requests.post(url, data=data)
    if resposta.status_code == 200:
        print("✅ Notificação enviada com sucesso!")
    else:
        print(f"❌ Erro ao enviar notificação! Código {resposta.status_code}")

# Teste de envio
enviar_notificacao("🚀 Sistema ativo! Monitoramento automático iniciado.")