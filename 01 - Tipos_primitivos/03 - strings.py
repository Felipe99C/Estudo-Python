
#%%
# Escreva um programa que receba uma string do usuário e a converta para maiúsculas.
texto = input(print("Insira o texto que deseja converter para maiúsculo: "))

print(f"\n{texto.upper()}")

#%%
# Crie um programa que receba o nome completo do usuário e imprima o nome com todas as letras minúsculas.

nome = input(print("Insira seu nome: "))

print(f"\n seu nome é : {nome.upper()}")


#%%
# Desenvolva um programa que peça ao usuário para inserir uma frase e, em seguida, imprima esta frase sem espaços em branco no início e no final.

#%%
# Faça um programa que peça ao usuário para digitar uma data no formato "dd/mm/aaaa" e, em seguida, imprima o dia, o mês e o ano separadamente.
data = input("insira uma data no formato dd/mm/aaaa: " )
lista_dia_mes_ano = data.split("/")
print(f"o elemento 1 é: {lista_dia_mes_ano[0]}")
print(f"o elemento 2 é: {lista_dia_mes_ano[1]}")
print(f"o elemento 3 é: {lista_dia_mes_ano[2]}")


#%%
# Escreva um programa que concatene duas strings fornecidas pelo usuário.