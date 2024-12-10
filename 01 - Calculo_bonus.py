# Cálculo de Bônus com Entrada do Usuário
# Escreva um programa em Python que solicita ao usuário para digitar seu nome, 
# o valor do seu salário mensal e o valor do bônus que recebeu. 
# O programa deve, então, imprimir uma mensagem saudando o usuário pelo nome e
# informando o valor do salário em comparação com o bônus recebido.

# Recebe o nome
nome = input("Insira o seu nome, por favor: ")

# Convertendo as entradas para float usando try/except para evitar erros
try:
    salario = float(input("\nAgora informe o seu salário R$: "))
    bonus_percentual = float(input("\nInforme o seu percentual de bônus para o calculo (%):  "))
    valor = 1000 + salario + (salario * (bonus_percentual/100))

    print(f"Parabéns {nome} o valor do seu salário com o bônus de {bonus_percentual}% é de: R$: {valor:.2f}")

except ValueError:
    print("\n Por favor insira apenas numeros para os valores de salário e Bônus! ")

# Agora identifique quais erros o código pode dar?

# entrada de formatos inválidos
# Não fazer a conversão para float
