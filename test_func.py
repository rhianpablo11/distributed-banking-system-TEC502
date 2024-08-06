from datetime import datetime

# Suponha que esta seja a data de criação da conta
data_criacao_conta = datetime(2023, 8, 1)

# Obtendo a data atual
data_atual = datetime.now()

# Calculando a diferença entre as datas
diferenca = data_atual - data_criacao_conta

# Obtendo o número de dias da diferença
dias_passados = diferenca.days

# Formatando as datas
data_criacao_conta_formatada = data_criacao_conta.strftime("%d/%m/%Y")
data_atual_formatada = data_atual.strftime("%d/%m/%Y")

print(f"Data de criação da conta: {data_criacao_conta_formatada}")
print(f"Data atual: {data_atual_formatada}")
print(f"Dias passados desde a criação da conta: {dias_passados} dias")