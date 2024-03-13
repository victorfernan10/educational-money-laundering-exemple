import json
from datetime import datetime

with open('config.json') as config_file:
    config = json.load(config_file)
valor_referencia_mensal = config["valor_referencia_mensal"]

with open('database.json', encoding='utf-8') as database_file:
    database = json.load(database_file)
produtos = database["produtos"]

def calcular_valor_total_mes():
    try:
        with open('vendas_gerais.txt') as vendas_file:
            vendas = vendas_file.readlines()
            valor_total_mes = sum(float(venda.split(' - ')[-1].split(': ')[-1].replace('R$', '').strip()) for venda in vendas)
            return valor_total_mes
    except FileNotFoundError:
        return 0

def calcular_valor_compra(codigos_produtos):
    total = 0
    for codigo in codigos_produtos:
        produto = next((p for p in produtos if p["cod_produto"] == codigo), None)
        if produto:
            total += produto["valor_real"]
    return total

def registrar_venda(valor_compra):
    hoje = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('vendas_gerais.txt', 'a') as vendas_file:
        vendas_file.write(f"{hoje} - Valor da compra: R${valor_compra}\n")

def main():
    valor_total_mes = calcular_valor_total_mes()
    print(f"Valor total do mês até o momento: R${valor_total_mes}")
    
    while True:
        codigos_produtos = input("Digite os códigos dos produtos separados por vírgula (ou 's' para sair): ").split(',')
        if 's' in codigos_produtos:
            break
        valor_compra = calcular_valor_compra([int(codigo) for codigo in codigos_produtos])
        print(f"Valor total da compra: R${valor_compra}")
        valor_total_mes += valor_compra
        registrar_venda(valor_compra)
        print(f"Valor total acumulado no mês: R${valor_total_mes}")
        verificar_meta(valor_total_mes)

def verificar_meta(valor_total_mes):
    if valor_total_mes >= valor_referencia_mensal:
        print("Parabéns! Você atingiu a meta mensal.") 

if __name__ == "__main__":
    main()
