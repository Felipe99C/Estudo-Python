### Exercício 21: Conversor de Temperatura

# Escreva um programa que converta a temperatura de Celsius para Fahrenheit.
# O programa deve solicitar ao usuário a temperatura em Celsius e, utilizando `try-except`, garantir que a entrada seja numérica, tratando qualquer `ValueError`.
# Imprima o resultado em Fahrenheit ou uma mensagem de erro se a entrada não for válida.

try:
    temp_c = float(input("Por favor insira a temperatura em Celsius: "))
    temp_f = 0
    temp_f = (temp_c * 1.8) + 32
    print(f"O valor da temperatura em Fahrenheit é de {temp_f} F")
except ValueError:
    print("Valor inserido não é válido, favor inserir somente numeros!")

#%%

### Exercício 22: Verificador de Palíndromo

# Crie um programa que verifica se uma palavra ou frase é um palíndromo (lê-se igualmente de trás para frente, desconsiderando espaços e pontuações).
# Utilize `try-except` para garantir que a entrada seja uma string. 
# Dica: Utilize a função `isinstance()` para verificar o tipo da entrada.


palavra = str(input("Insira uma palavra:").strip().lower())
palavra_reverso = palavra[::-1]
if isinstance(palavra, str):
    try:
        if palavra_reverso == palavra:
            print(f"A palavra digitada {palavra} é uma Palindromo!")
        else:
            print(f"A palavra digitada {palavra_reverso} não é um palindromo")
    except TypeError:
        print("Valor inserido não é valido")
else:
    print("O valor digitado não é uma palavra!")

# %%
