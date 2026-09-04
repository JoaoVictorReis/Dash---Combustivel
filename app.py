#Aqui é onde geramos o dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

estado = sorted(tabela['estado'].unique())
estado_selecionado = st.sidebar.selectbox("Estados", estado, index=None)

data_min = tabela['data_coleta'].min()
data_max = tabela['data_coleta'].max()
periodo_selecionado = st.sidebar.date_input("Período", [data_min, data_max], min_value=data_min, max_value=data_max)

#Existe uma chance do usuario não selecionar nenhum produto e nem estado, pensando assim o pandas deve considerar que todos os valores devem ser considerados.
if produto_selecionado is not None:
    tabela = tabela[tabela['produto'] == produto_selecionado]

if estado_selecionado is not None:
    tabela = tabela[tabela['estado'] == estado_selecionado] #Aqui eu poderia ter usado um .query().

#Aqui estamos filtrando a tabela e puxando apenas os valores que estão dentro do período selecionado.
if len(periodo_selecionado) == 2:
    tabela = tabela[(tabela['data_coleta'] >= pd.to_datetime(periodo_selecionado[0])) & (tabela['data_coleta'] <= pd.to_datetime(periodo_selecionado[1]))]
# Aqui estamos utilizando um filtro booleano para selecionar apenas as linhas que estão dentro do período selecionado, utilizando o operador & para fazer a interseção das duas condições.


#Criando uma tabela de resumo com as informações que queremos exibir no dashboard
resumo = tabela.groupby(['produto', 'estado']).agg({'preco_venda': ['mean']}).reset_index()

#resumo = tabela.groupby(['produto', 'estado']).mean(numeric_only=True).reset_index() <= Não funciona tão bem, pois o mean() não permite que você selecione apenas uma coluna para calcular a média, ai acaba que a média é calculada em até colunas que não fazem sentido.
#resumo = tabela.gorupby(['produto', 'estado'])['preco_venda'].mean().reset_index() <= Seria a forma correta utilizando o .mean(), mas o .agg() é mais flexível, pois permite que você selecione várias colunas e aplique diferentes funções de agregação em cada uma delas, além de permitir que você renomeie as colunas resultantes.

st.header("Resumo de Preços por Produto e Estado")
st.dataframe(resumo.style.format({('preco_venda', 'mean'): "R${:,.2f}"}), use_container_width=True)


#gerando um gráfico de comparação entre valores 
st.header("Comparação de Preços")
st.subheader("Aqui comparamos os preços médios dos combustiveis com base nos valores anteriores.")
velocimetro = go.Figure(go.Indicator(mode = "gauge+number" , 
                                        value= resumo[('preco_venda', 'mean')].mean(), 
                                        number={'prefix': "R$", 'valueformat': ".2f"},
                                        title={'text': "Preço Médio"}, 
                                        gauge={'axis': {'range': [resumo[('preco_venda', 'mean')].min(), resumo[('preco_venda', 'mean')].max()], 'tickprefix': "R$", 'tickformat': ".2f"},
                                               'bar': {'color': "blue"}}))

st.plotly_chart(velocimetro, use_container_width=True)


#agrupar por data e produto, para gerar um gráfico de linha mostrando a evolução do preço médio ao longo do tempo.

linhadotempo = tabela.groupby(['data_coleta', 'produto'])['preco_venda'].mean().reset_index()

linhasgraph = px.line(linhadotempo, x='data_coleta', y=('preco_venda'), color='produto', title="Evolução do Preço Médio ao Longo do Tempo")
st.plotly_chart(linhasgraph, use_container_width=True)

