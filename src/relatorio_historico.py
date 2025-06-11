import json
import re
import matplotlib.pyplot as plt
from datetime import datetime

# Simulação de mensagens do grupo (exemplo)
mensagens = [
    "EUR/USD 5M 14:05 CALL - PRIMÁRIO",
    "GBP/JPY 5M 14:10 PUT - GALE 1",
    "EUR/USD 5M 14:20 PUT - PRIMÁRIO",
    "USD/CAD 5M 14:25 CALL - GALE 2"
]

# Configurações iniciais
saldo_inicial = 500
saldo = saldo_inicial
ganhos_totais = 0
perdas_totais = 0
qtd_sinais = 0
lucros_diarios = []  # Garante que a variável está definida corretamente
valores = {"PRIMÁRIO": 10, "GALE 1": 20, "GALE 2": 40}
ganhos = {"PRIMÁRIO": 9, "GALE 1": 18, "GALE 2": 36}  # 90% retorno

# Regex para capturar tipo de entrada
secao_re = re.compile(r"(PRIMÁRIO|GALE 1|GALE 2)")

# Processamento dos sinais
for msg in mensagens:
    match = secao_re.search(msg)
    if match:
        secao = match.group(1)
        saldo += ganhos[secao]
        ganhos_totais += ganhos[secao]
        qtd_sinais += 1
        lucros_diarios.append(saldo)  # Adicionando saldo atualizado ao histórico

# Garantir que há pelo menos um valor antes de gerar o gráfico
if not lucros_diarios:
    lucros_diarios = [saldo_inicial]  # Adiciona saldo inicial para evitar erro

# Projeções futuras
media_lucro_diario = ganhos_totais if qtd_sinais else 1
meta_10k = int((10000 - saldo_inicial) / media_lucro_diario) if media_lucro_diario else '∞'
meta_100k = int((100000 - saldo_inicial) / media_lucro_diario) if media_lucro_diario else '∞'
meta_1m = int((1000000 - saldo_inicial) / media_lucro_diario) if media_lucro_diario else '∞'

# Geração do relatório JSON
relatorio = {
    "data": datetime.now().strftime("%Y-%m-%d"),
    "sinais_processados": qtd_sinais,
    "lucro_total": ganhos_totais,
    "saldo_final": saldo,
    "projecao_10k_dias": meta_10k,
    "projecao_100k_dias": meta_100k,
    "projecao_1m_dias": meta_1m
}

with open(f"reports/historico/{relatorio['data']}_resumo.json", "w") as f:
    json.dump(relatorio, f, indent=4)

# Geração do gráfico
plt.plot(lucros_diarios, marker="o")
plt.title("Evolução do Saldo")
plt.xlabel("Operações")
plt.ylabel("Saldo Atual")
plt.grid(True)
plt.savefig(f"reports/historico/{relatorio['data']}_grafico.png")  # Garante que o gráfico será salvo corretamente
plt.close()

print(f"✅ Relatório e gráfico gerados com sucesso! 🚀")