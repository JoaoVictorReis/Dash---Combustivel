import pandas as pd
from leitura import DIR_RAW, DIR_PROCESS, gerar_dados_exemplo

def validar_diretorios():
    arquivoscsv = list(DIR_RAW.glob("*.csv"))
    if not arquivoscsv:
        print(f"Nenhuma base de dados encontrada. Criaremos uma base de exmplo para você testar o pipeline.")
        gerar_dados_exemplo().to_csv(DIR_RAW / "base_exemplo.csv", index=False)
        
    return carregar_dados_brutos()

def carregar_dados_brutos():
    arquivoscsv = list(DIR_RAW.glob("*.csv"))
    tabelas = []
    
    for arquivo in arquivoscsv:
        print(f"Lendo arquivo: {arquivo.name}")
        tabelas.append(pd.read_csv(arquivo))

    return pd.concat(tabelas, ignore_index=True)

def transformar_dados(tabela: pd.DataFrame):
    #converte as datas
    if not pd.api.types.is_datetime64_any_dtype(tabela["data_coleta"]):
        tabela["data_coleta"] = pd.to_datetime(tabela["data_coleta"], errors="coerce", format="mixed") #converte para data e indica que a data vem primeiro, se não for algo valido transforma em NaT. 
        
    # Quero que a coluna de preço seja float, mas alguns arquivos podem vir com vírgula, então vou substituir a vírgula por ponto e converter para float.
    if tabela["preco_venda"].dtype != "float64" or tabela["preco_venda"].astype(str).str.contains(",").any():
        tabela["preco_venda"] = tabela["preco_venda"].astype(str).str.replace(",", "." , regex=False).astype(float) #converte para float, substituindo vírgula por ponto.

    #remover linhas com preço ou data nulos, usando intertuples.
    antes = len(tabela)
    for linhas in tabela.itertuples():
        if pd.isna(linhas.preco_venda) or pd.isna(linhas.data_coleta):
           tabela = tabela.drop(linhas.Index) #remove linhas com preço e data nulos.
    #da para fazer isso diretamente com o dropna e o subset, mas estou fazendo assim para treinar o intertuples.
    if antes != len(tabela):
        print(f"Removidas {antes - len(tabela)} linhas com preço ou data nulos.")
    
    #remover duplicatas
    tabela = tabela.drop_duplicates() 
    
    #remover linhas com preçoes absurdos, como preço negativo ou maior que 15 reais.
    tabela = tabela[(tabela["preco_venda"] >= 0) & (tabela["preco_venda"] <= 15)] #utilizando o operador & para fazer a interseção das duas condições, assim removendo os preços absurdos.
    #"Pandas, pegue a tabela, salve apenas as linhas que deram True e jogue fora as que deram False" se chama filtro booleano ou indexação condicional.
    
    #formatação do texto, para evitar problemas de inconsistência de maiúsculas e minúsculas, espaços em branco, etc.
    for col in ["regiao", "estado", "municipio", "produto", "unidade", "bandeira"]:
        if col in tabela.columns:
            tabela[col] = tabela[col].astype(str).str.strip().str.upper() #remove espaços e coloca tudo em maiúsculo.
    
    #gerar colunas auxiliares, como ano, mês, dia da semana.
    tabela["ano"] = tabela["data_coleta"].dt.year
    tabela["mes"] = tabela["data_coleta"].dt.month 
    tabela["ano_mes"] = tabela["data_coleta"].dt.to_period("M").astype(str) #ano e mês juntos, para facilitar a agregação.

    return tabela



tabela_bruta = validar_diretorios()
tabela_processada = transformar_dados(tabela_bruta)
tabela_processada.to_csv(DIR_PROCESS / "tabela_processada.csv", index=False)

Caminho_Processado= {DIR_PROCESS / 'tabela_processada.csv'}
print(f"Tabela processada salva em {Caminho_Processado}")


