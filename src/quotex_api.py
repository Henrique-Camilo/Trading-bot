from quotexapi import QuotexAPI

# Informações da sua conta da Quotex
email = "sebastiao.henriue.camilo@gmail.com"
senha = "Dps@824616*"

# Criar conexão com a API
api = QuotexAPI(email, senha)

# Testar conexão
if api.connect():
    print("✅ Conectado à API da Quotex!")

    # Obter informações sobre os ativos disponíveis
    ativos = api.get_assets()
    print("🧐 Ativos disponíveis:", ativos)

    # Exemplo: Comprar 1 unidade no par EUR/USD
    api.buy("EUR/USD", 1, "CALL", 60)
    print("✅ Ordem enviada para EUR/USD!")

else:
    print("⚠️ Falha na conexão. Verifique suas credenciais.")
