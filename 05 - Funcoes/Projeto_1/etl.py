#aqui vão ficar todos os processos da minha ETL

import csv



def ler_csv(nome_arquivo_csv: str) -> list[dict]:
    #ler um arquivo csv e retorna uma lista de dicionarios.

    lista = [] # cria uma lista vazia

    with open (nome_arquivo_csv, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            lista.append(linha)
    return lista

def filtrar_produtos_N_entregues(lista: list[dict]) -> list[dict]:
    #Filtras Produtos com entrega igual a false.

    lista_n_entregues = [] # cria uma lista vazia
    for produto in lista:
        if produto.get("entregue") == 'True':
            lista_n_entregues.append(produto)
    return lista_n_entregues


def soma_valores_dos_produtos(produtos_nao_entregues: list[dict]) -> int:

    valor_total = 0
    for produto in produtos_nao_entregues:
        valor_total += int(produto.get("preco"))
    return valor_total

