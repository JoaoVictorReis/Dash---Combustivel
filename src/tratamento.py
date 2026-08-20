import pandas as pd
from leitura import DIR_RAW, DIR_PROCESS, gerar_dados_exemplo


#Anotação: gerar uma função que apenas verifica se o arquivo existe, caso não exista, chama a função gerar_dados_exemplo().
def carregar_dados_brutos():
    arquivoscsv = list(DIR_RAW.glob("*.csv"))
    
    tabelas = []
    if not arquivoscsv:
        print("Nenhum arquivo CSV encontrado em", DIR_RAW)
        print("Gerando dados de exemplo...")
        gerar_dados_exemplo().to_csv(DIR_RAW / "dados_exemplo.csv", index=False)
        arquivoscsv = [DIR_RAW / "dados_exemplo.csv"]
    
    for arquivo in arquivoscsv:
        print(f"Lendo arquivo: {arquivo.name}")
        tabelas.append(pd.read_csv(arquivo))

    return pd.concat(tabelas, ignore_index=True)

def transformar_dados(tabela: pd.DataFrame):
    #converte as datas
    if not pd.api.types.is_datetime64_any_dtype(tabela["data_coleta"]):
        tabela["data_coleta"] = pd.to_datetime(tabela["data_coleta"], errors="coerce", dayfirst=True) #converte para data e indica que a data vem primeiro, se não for algo valido transforma em NaT. 
        
    if tabela["preco_venda"].dtype != "float64":
        tabela["preco_venda"] = tabela["preco_venda"].astype(str).str.replace(",", "." , regex=False).astype(float), errors="coerce" #converte para float, substituindo vírgula por ponto.


