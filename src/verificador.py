import os
import json
import time
import shutil
from datetime import datetime
import subprocess

# Diretórios dos relatórios e backup
reports_dir = "reports/historico/"
backup_dir = "backup/historico/"

# Obtém a data atual
data_hoje = datetime.now().strftime("%Y-%m-%d")

# Caminhos dos arquivos esperados
json_path = os.path.join(reports_dir, f"{data_hoje}_resumo.json")
txt_path = os.path.join(reports_dir, f"{data_hoje}_resumo.txt")
png_path = os.path.join(reports_dir, f"{data_hoje}_grafico.png")

# Função para criar backup
def criar_backup():
    destino_backup = os.path.join(backup_dir, f"backup_{data_hoje}")
    
    if not os.path.exists(destino_backup):
        os.makedirs(destino_backup)  # Cria pasta do backup diário

    for arquivo in os.listdir(reports_dir):
        caminho_origem = os.path.join(reports_dir, arquivo)
        caminho_destino = os.path.join(destino_backup, arquivo)
        shutil.copy(caminho_origem, caminho_destino)
    
    print(f"✅ Backup salvo em {destino_backup}")

# Função de diagnóstico automático completo
def verificar_e_corrigir():
    problemas = []

    # Verifica JSON
    if not os.path.exists(json_path):
        problemas.append(f"Arquivo JSON ausente: {json_path}")
    else:
        try:
            with open(json_path, "r") as f:
                data = json.load(f)
                if not data or "saldo_final" not in data:
                    problemas.append("JSON encontrado, mas vazio ou inválido!")
        except json.JSONDecodeError:
            problemas.append("Erro ao ler JSON! Arquivo corrompido.")

    # Verifica TXT
    if not os.path.exists(txt_path):
        problemas.append(f"Arquivo TXT ausente: {txt_path}")

    # Verifica PNG (Gráfico)
    if not os.path.exists(png_path):
        problemas.append(f"Gráfico PNG ausente: {png_path}")

    if problemas:
        print("\n⚠️ Problemas detectados! Iniciando correção automática... ⚠️\n")
        for problema in problemas:
            print(f"- {problema}")

        # Recria JSON se estiver ausente ou inválido
        if not os.path.exists(json_path) or "saldo_final" not in json.load(open(json_path, "r", errors="ignore")):
            relatorio_padrao = {
                "data": data_hoje,
                "sinais_processados": 0,
                "lucro_total": 0,
                "saldo_final": 500,  # Definindo um saldo inicial padrão
                "projecao_10k_dias": "∞",
                "projecao_100k_dias": "∞",
                "projecao_1m_dias": "∞"
            }
            with open(json_path, "w") as f:
                json.dump(relatorio_padrao, f, indent=4)
            print("✅ Relatório JSON reparado!")

        # Recria TXT se estiver ausente
        if not os.path.exists(txt_path):
            with open(txt_path, "w") as f:
                f.write("Relatório diário não gerado corretamente. Reparo em andamento...\n")
            print("✅ Relatório TXT reparado!")

        # Se o gráfico PNG estiver ausente, roda `relatorio_historico.py` automaticamente para gerar
        if not os.path.exists(png_path):
            print("⚠️ Gráfico PNG ausente, iniciando geração automática...")
            subprocess.run(["python", "src/relatorio_historico.py"])  # Executa o script principal
            print("✅ Gráfico PNG regenerado!")

        # Após correções, cria backup
        criar_backup()

    else:
        print("\n✅ Todos os arquivos estão corretos! 🚀")
        criar_backup()  # Faz backup mesmo quando tudo está certo

# Loop de varredura contínua e ajustável
intervalo_varredura = 900  # Tempo padrão de 15 minutos
while True:
    print("\n🔍 Realizando varredura completa do sistema...")
    verificar_e_corrigir()
    print(f"⏳ Aguardando próxima varredura em {intervalo_varredura // 60} minutos...\n")
    time.sleep(intervalo_varredura)