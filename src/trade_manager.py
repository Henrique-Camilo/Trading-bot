# src/trade_manager.py

from config import SALDO_INICIAL, STOP_LOSS_PORCENTAGEM, LUCRO_DIARIO_PORCENTAGEM
from bot import enviar_mensagem

saldo = SALDO_INICIAL
lucro_acumulado = 0

def executar_trade(sinal):
    """ Executa a operação de trade baseada nos sinais """
    global saldo, lucro_acumulado

    valor_entrada = saldo * 0.10
    resultado = "win"  # Simulação de resultado

    if resultado == "win":
        lucro = valor_entrada * 0.95
        saldo += lucro
        lucro_acumulado += lucro
    else:
        saldo -= valor_entrada

    enviar_mensagem(f"Sinal: {sinal}\n💰 Saldo atual: {saldo:.2f} USD")

    # Verificar Stop Loss e Meta de Lucro
    if saldo <= SALDO_INICIAL * STOP_LOSS_PORCENTAGEM:
        enviar_mensagem("🚨 Stop Loss atingido. Parando operações.")
        return False

    if lucro_acumulado >= SALDO_INICIAL * LUCRO_DIARIO_PORCENTAGEM:
        enviar_mensagem("✅ Meta de lucro diário atingida!")
        return False

    return True

if __name__ == "__main__":
    print("🔄 Testando execução de trade...")
    executar_trade("USD/TRY;19:05;PUT")