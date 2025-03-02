# O principal uso das Funções são para facilitar nossa vida sempre que identificarmos um processo que é reutilizavel em outras partes do programa.
#  dividindo o código em partes menores e mais gerenciavel evitando repetição de código sem necessidade.

# Definindo Funções

 #Para criar uma função em Python, você usa a keyword def, seguida de um nome de função, parênteses () contendo zero ou mais "parâmetros", e dois pontos :.
 #  O bloco de código indentado que segue é o corpo da função.

#exemplo

def soma(valor_1, valor_2):
    resultado = valor_1 + valor_2
    return resultado 

print(soma(3,2))

#aplicando type hint a essa função
#indica que esperamos valores do tipo float de entrada e que a saida será um float tbm, se não passar nada o padrao vai ser 10
def soma2(valor_1 : float, valor_2 : float = 10) -> float:
    resultado = valor_1 + valor_2
    return resultado

print(soma2(5,7))


## Nomes de Funções
#Os nomes das funções seguem as mesmas regras de nomes de variáveis em Python: podem conter letras, números (não como primeiro caractere) e underscores (_), mas não espaços ou caracteres especiais. Nomes de funções devem ser descritivos e, por convenção, utilizam snake_case.

#Parâmetros e Argumentos
#Parâmetros são as variáveis listadas nos parênteses na definição da função. Eles são como placeholders para os dados que a função irá processar.

#Argumentos são os valores reais passados para a função quando ela é chamada.
def soma(a, b):
    return a + b

#########################################

### Palavras-chave importantes
# def inicia a definição de uma função.
# return é usado para retornar um valor da função. Se omitido, a função retorna None por padrão.
# pass pode ser usado como um placeholder para uma função vazia, significando "nada".


################################# Exercicios #####################################################

#%%
# 1 Calcular Média de Valores em uma Lista

from typing import List

def calcular_media(valores: List[float]) -> float:
    return sum(valores) / len(valores)

lista = [1,4,5,2,6,8,2]

print(calcular_media(lista))

#%%

#Contar Valores Únicos em uma Lista
def contar_valores_unicos(lista: List[int]) -> int:
    return len(set(lista)) # a função set já retorna valores unicos

#%%

# Calcular Desvio Padrão de uma Lista

#desvio padrão é uma medida de dispersão que indica o quanto os valores de um conjunto de dados se afastam da média.


def calcular_desvio_padrao(valores: List[float]) -> float:
    media = sum(valores) / len(valores)
    variancia = sum((x - media) ** 2 for x in valores) / len(valores)
    return variancia ** 0.5

dados = [10, 12, 23, 23, 16, 23, 21, 16]
print(calcular_desvio_padrao(dados))

#%%

# Encontrar Valores Ausentes em uma Sequência

def encontrar_valores_ausentes(sequencia: List[int]) -> List[int]:
    lista_completa = set(range(min(sequencia), max(sequencia) + 1))
    return list(lista_completa - set(sequencia))


numero = [1,3,6,12]
print(encontrar_valores_ausentes(numero))


