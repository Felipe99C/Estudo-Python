from etl import pipeline_calcular_kpi_vendas

pasta: str = 'data'
formato_saida = ['csv', 'parquet']

pipeline_calcular_kpi_vendas(pasta, formato_saida)