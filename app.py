#Aqui é onde geramos o dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

#Determinando o caminho do arquivo processado
CAMINHO = Path(__file__).resolve().parent / "DATA" / "PROCESSED" / "tabela_processada.csv"

if not CAMINHO.exists():
    st.error("Arquivo processado não encontrado. Por favor, execute o pipeline de tratamento de dados primeiro.")
    
    
    
    
    
    