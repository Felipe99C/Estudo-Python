# O principal uso das Funções são para facilitar nossa vida sempre que identificarmos um processo que é reutilizavel em outras partes do programa.
#  dividindo o código em partes menores e mais gerenciavel evitando repetição de código sem necessidade.
# 

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


