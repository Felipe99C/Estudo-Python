############################ Projeto ##################################
#%%

"""
Desafio: Análise de Vendas de Produtos Objetivo: Dado um arquivo CSV contendo dados de vendas de produtos,
o desafio consiste em ler os dados, processá-los em um dicionário para análise e, 
por fim, calcular e reportar as vendas totais por categoria de produto.

"""

from etl import ler_csv, filtrar_produtos_N_entregues, soma_valores_dos_produtos   

file_path = r'D:\Estudos\Python\Estudo-Python\05 - Funcoes\Projeto_1\vendas.csv'

lista_de_produtos = ler_csv(file_path)
produtos_nao_entregues = filtrar_produtos_N_entregues(lista_de_produtos)
valor_produtos_entregues = soma_valores_dos_produtos(produtos_nao_entregues)
print(valor_produtos_entregues)