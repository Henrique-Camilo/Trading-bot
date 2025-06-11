import os
import logging
from datetime import datetime

# Configuração do diretório dos logs
log_dir = "logs/"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Nome do arquivo de log baseado na data atual
log_filename = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d')}.txt")

# Configuração do Logger
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Função para registrar eventos no log
def registrar_evento(mensagem, nivel="INFO"):
    if nivel == "ERROR":
        logging.error(mensagem)
    elif nivel == "WARNING":
        logging.warning(mensagem)
    else:
        logging.info(mensagem)

# Teste de eventos no log
registrar_evento("🔍 Sistema de logs iniciado!", "INFO")
registrar_evento("✅ Backup realizado com sucesso!", "INFO")
registrar_evento("⚠️ Arquivo JSON corrompido! Correção em andamento...", "WARNING")
registrar_evento("❌ Falha na geração do gráfico PNG!", "ERROR")

print(f"✅ Logs registrados em {log_filename}")