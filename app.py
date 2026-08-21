#Aqui é onde geramos o dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

#Determinando o caminho do arquivo processado
# Precisamos dessa constante para criar a função que ira ler o arquivo processado.
CAMINHO = Path(__file__).resolve().parent / "DATA" / "PROCESSED" / "tabela_processada.csv"

#Criamos uma exceção para garantir que o arquivo processado exista antes de prosseguir com a execução do dashboard
try:
    if not CAMINHO.exists():
        raise FileNotFoundError("Arquivo processado não encontrado. Por favor, execute o pipeline de tratamento de dados primeiro.")

except FileNotFoundError as e:
    print(e)
    exit()

#Preciamos de uma função que leia o arquivo para que possamos utilizar os dados no dashboard. A função abaixo faz exatamente isso.
#vamos carregar o arquivo processado
@st.cache_data
def carregar_dados(CAMINHO):
    tabela = pd.read_csv(CAMINHO, parse_dates=['data_coleta'])
    return tabela
# A função esta autoexplicativa, mas para reforçar.
# o ST.cache serve para armazenar os dados da planilha, evitando que o streamlit releia a tabela toda vez que houver uma interação com o dashboard, melhorando a performance do mesmo.
# A função read_csv literalmente é utilizada para ler arquivos CSV. o parse_dates é utilizado para informar ao python que a coluna data_coleta deve ser interpretada como uma coluna de datas, e não como uma string.
tabela = carregar_dados(CAMINHO)

#Daqui para frente começa a execução do dashboard
st.set_page_config(page_title="Dashboard de Análise de Dados", layout="wide")

#vamos criar os filtros para o dashboard
st.sidebar.header("Filtros")

produtos = sorted(tabela['produto'].unique())
produto_selecionado = st.sidebar.selectbox("Produtos", produtos, index=None)







   
    
    