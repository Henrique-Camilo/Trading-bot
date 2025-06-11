# run.py

from src.signal_reader import ler_sinais
from src.trade_manager import executar_trade
import time
from config import CHECK_INTERVAL

print("🚀 Bot de Trading iniciado...")

while True:
    sinais = ler_sinais()
    for sinal in sinais:
        continuar = executar_trade(sinal)
        if not continuar:
            print("❌ Encerrando operações por limite atingido.")
            exit()
    time.sleep(CHECK_INTERVAL)  # Espera 30 segundos antes de buscar novos sinais