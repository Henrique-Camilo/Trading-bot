import re
import json
from datetime import datetime

# Simulação de sinais recebidos
mensagens = [
    "EUR/USD 5M 14:05 CALL - PRIMÁRIO",
    "GBP/JPY 5M 14:10 PUT - GALE 1",
    "EUR/USD 5M 14:20 PUT - PRIMÁRIO",
    "USD/CAD 5M 14:25 CALL - GALE 2"
]

# Configuração inicial
saldo_inicial = 500
saldo = saldo_inicial
lucros_diarios = []  # Lista para armazenar evolução do saldo
valores = {"PRIMÁRIO": 10, "GALE 1": 20, "GALE 2": 40}
ganhos = {"PRIMÁRIO": 9, "GALE 1": 18, "GALE 2": 36}  # Retorno de 90%

# Regex para capturar sinais corretamente
sinal_re = re.compile(r"(EUR/USD|GBP/JPY|USD/CAD).*?(CALL|PUT).*?(PRIMÁRIO|GALE 1|GALE 2)")

# Processamento dos sinais
for msg in mensagens:
    match = sinal_re.search(msg)
    if match:
        ativo = match.group(1)
        direcao = match.group(2)
        tipo = match.group(3)
        saldo += ganhos[tipo]
        lucros_diarios.append(saldo)

# Garante que há pelo menos um valor antes de gerar previsão
if not lucros_diarios:
    lucros_diarios = [saldo_inicial]

# Projeções futuras
media_lucro_diario = sum(lucros_diarios) / len(lucros_diarios)
meta_10k = int((10000 - saldo_inicial) / media_lucro_diario) if media_lucro_diario else '∞'
meta_100k = int((100000 - saldo_inicial) / media_lucro_diario) if media_lucro_diario else '∞'
meta_1m = int((1000000 - saldo_inicial) / media_lucro_diario) if media_lucro_diario else '∞'

# Geração do relatório atualizado
relatorio = {
    "data": datetime.now().strftime("%Y-%m-%d"),
    "ativos_analisados": len(mensagens),
    "lucro_total": saldo - saldo_inicial,
    "saldo_final": saldo,
    "projecao_10k_dias": meta_10k,
    "projecao_100k_dias": meta_100k,
    "projecao_1m_dias": meta_1m
}

with open(f"reports/historico/{relatorio['data']}_sinais.json", "w") as f:
    json.dump(relatorio, f, indent=4)

print("✅ Processamento de sinais concluído com sucesso! 🚀")