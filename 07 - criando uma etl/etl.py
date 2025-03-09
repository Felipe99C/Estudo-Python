import pandas as pd
import os
import glob
from loguru import logger
from log import log_decorator


logger.add(r"D:\Estudos\Python\Estudo-Python\07 - criando uma etl\meus_logs.log", format="{time} {level} {message} {file} {line}", level="CRITICAL")
# ler e consolidar os arquivos Json num dataframe.

@log_decorator
def extrair_dados(pasta: str) -> pd.DataFrame:
    arquivos_json = glob.glob(os.path.join(pasta, '*.json'))

    if not arquivos_json:
        logger.error(f"Nenhum arquivo JSON encontrado na pasta: {pasta}")
        # Você pode escolher retornar um DataFrame vazio ou lançar uma exceção
        return pd.DataFrame()

    df_list = [pd.read_json(arquivo) for arquivo in arquivos_json]
    df_total = pd.concat(df_list, ignore_index=True)
    logger.info('\n Dados extraídos com sucesso')
    return df_total


# realizar as transformaçoes nescessárias

@log_decorator
def calcular_kpi_total_de_vendas(df: pd.DataFrame) -> pd.DataFrame:
    df_novo = df.copy() # cria uma cópia para não alterar o df original
    df_novo['Total'] = df['Venda'] * df['Quantidade'] # cria a coluna total  no novo dataframe com o valor da venda multiplicado pela quantidade
    return df_novo

# carregar os dados transformados

@log_decorator
def carregar_dados(df: pd.DataFrame, formato_saida: list): 
    for formato in formato_saida:
        if formato not in ['csv', 'parquet']:
            logger.error(f'Formato de saída {formato} não suportado')
            continue  # Pula para o próximo formato
        if formato == 'csv':
            df.to_csv('dados_transformados.csv',index=False)
            logger.info('Dados salvos em CSV')
        elif formato == 'parquet':  # Use 'elif' para evitar verificações desnecessárias
            df.to_parquet('dados_transformados.parquet')
            logger.info('Dados salvos em Parquet')

@log_decorator
def pipeline_calcular_kpi_vendas(pasta: str, formato_saida: list):
    df = extrair_dados(pasta)
    df_calculado = calcular_kpi_total_de_vendas(df)
    carregar_dados(df_calculado, formato_saida)


    
