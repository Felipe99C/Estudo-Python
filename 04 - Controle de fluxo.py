#%%

# Exercício 2: Classificação de Dados de Sensor
#Imagine que você está trabalhando com dados de sensores IoT. 
# Os dados incluem medições de temperatura. 
# Você precisa classificar cada leitura como 'Baixa', 'Normal' ou 'Alta'. Considerando que:

#Temperatura < 18°C é 'Baixa'
#Temperatura >= 18°C e <= 26°C é 'Normal'
#Temperatura > 26°C é 'Alta'


temp = float(input("insira a temperatura: "))

if temp < 18:
    print("Temperatura baixa")
elif temp >= 18 and temp <= 26:
    print("Temperatura Normnal")
else:
    print("temperatura alta")

#%%

    #Exercício 3: Filtragem de Logs por Severidade
    # Você está analisando logs de uma aplicação e precisa filtrar mensagens com severidade 'ERROR'.
    # Dado um registro de log em formato de dicionário como log = {'timestamp': '2021-06-23 10:00:00', 'level': 'ERROR', 'message': 'Falha na conexão'},
    # escreva um programa que imprima a mensagem se a severidade for 'ERROR'.

log = {'timestamp': '2021-06-23 10:00:00', 'level': 'ERROR', 'message': 'Falha na conexão'}

if log['level'] == 'ERROR':
    print(log['message'])
else:
    print("Nenhum log de erro encontrado.")


#%% 

# Lista de logs
logs = [
    {'timestamp': '2021-06-23 10:00:00', 'level': 'ERROR', 'message': 'Falha na conexão'},
    {'timestamp': '2021-06-23 10:05:00', 'level': 'INFO', 'message': 'Conexão bem-sucedida'},
    {'timestamp': '2021-06-23 10:10:00', 'level': 'ERROR', 'message': 'Timeout na requisição'}
]

for log in logs:
    if log['level'] == 'ERROR':
        print(log['message'])
 
#%%

#Exercício 4: Validação de Dados de Entrada
# Antes de processar os dados de usuários em um sistema de recomendação, 
# você precisa garantir que cada usuário tenha idade entre 18 e 65 anos e tenha fornecido um email válido.
# Escreva um programa que valide essas condições e imprima "Dados de usuário válidos" ou o erro específico encontrado.

idade = int(input("Informe a sua indade: "))
email = input("Informe seu e-mail: ")

if idade < 18 and idade > 65:
    print("Idade fora do intervalo permitido")
elif "@" not in email or "." not in email:
    print("forneça um e-mail válido")
else:
    print("Dados de usuário válidos")