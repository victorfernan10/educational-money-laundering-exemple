import json
import random
from datetime import datetime

with open('config.json') as config_file:
    config = json.load(config_file)
valor_referencia_mensal = config["valor_referencia_mensal"]
limite_superior_referencia = valor_referencia_mensal * random.uniform(1, 1.20)

with open('database.json', encoding='utf-8') as database_file:
    database = json.load(database_file)
produtos = database["produtos"]

chances_combinacoes = {
    (produto["cod_produto"],): 0.5 for produto in produtos
}

for i, produto1 in enumerate(produtos):
    for j, produto2 in enumerate(produtos):
        if i < j:
            combinacao = (produto1["cod_produto"], produto2["cod_produto"])
            chances_combinacoes[combinacao] = 0.1

for i, produto1 in enumerate(produtos):
    for j, produto2 in enumerate(produtos):
        for k, produto3 in enumerate(produtos):
            if i < j < k:
                combinacao = (produto1["cod_produto"], produto2["cod_produto"], produto3["cod_produto"])
                chances_combinacoes[combinacao] = 0.1

def adicionar_produtos_aleatorios():
    valor_total_mes = 0
    produtos_adicionados = []
    while valor_total_mes < limite_superior_referencia:
        data_hora = datetime.now().replace(hour=random.randint(8, 20), minute=random.randint(0, 59), second=random.randint(0, 59))
        combinacao = random.choices(list(chances_combinacoes.keys()), weights=chances_combinacoes.values(), k=1)[0]
        valor_compra = sum(produto["valor_real"] for produto in produtos if produto["cod_produto"] in combinacao)
        produtos_adicionados.append((data_hora.strftime('%Y-%m-%d %H:%M:%S'), combinacao, valor_compra))
        valor_total_mes += valor_compra
    return produtos_adicionados

produtos_adicionais = adicionar_produtos_aleatorios()
with open('compras_declaradas.log', 'a') as compras_declaradas_file:
    for produto in produtos_adicionais:
        combinacao_nomes = ', '.join(produto["nome_produto"] for codigo_produto in produto[1] for produto in produtos if produto["cod_produto"] == codigo_produto)
        compras_declaradas_file.write(f"{produto[0]} - Produtos: {combinacao_nomes} - Valor: R${produto[2]}\n")

valor_total_mes = sum(produto[2] for produto in produtos_adicionais)

print("Produtos adicionados para atingir a meta mensal.")
print(f"Valor total acumulado no mês (com produtos adicionais): R${valor_total_mes}")
