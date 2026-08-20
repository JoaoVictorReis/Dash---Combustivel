from pathlib import Path
import pandas as pd
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW= RAIZ / "DATA" / "RAW"
DIR_PROCESS= RAIZ / "DATA" / "PROCESSED"


def gerar_dados_exemplo(n_linhas: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    Gera um DataFrame fake, mas com a mesma estrutura dos dados da ANP,
    pra você conseguir testar o pipeline inteiro (transform + dashboard)
    ANTES de baixar os dados reais.

    Depois é só trocar por `ler_csv_anp(caminho_do_arquivo_real)`.
    """
    rng = np.random.default_rng(seed)

    estados = ["SP", "RJ", "MG", "RS", "BA", "PR", "PE", "CE"]
    produtos = ["GASOLINA", "ETANOL", "DIESEL S10", "GNV"]
    bandeiras = ["PETROBRAS", "IPIRANGA", "RAIZEN", "BANDEIRA BRANCA"]

    datas = pd.date_range("2023-01-01", "2024-12-31", freq="W")

    df = pd.DataFrame({
        "regiao": rng.choice(["SE", "S", "NE", "N", "CO"], n_linhas),
        "estado": rng.choice(estados, n_linhas),
        "municipio": "Cidade " + rng.integers(1, 50, n_linhas).astype(str),
        "produto": rng.choice(produtos, n_linhas),
        "data_coleta": rng.choice(datas, n_linhas),
        "unidade": "R$/litro",
        "bandeira": rng.choice(bandeiras, n_linhas),
    })

    # Preço base por produto + ruído + leve tendência de alta ao longo do tempo
    preco_base = df["produto"].map({
        "GASOLINA": 5.60, "ETANOL": 3.90, "DIESEL S10": 5.90, "GNV": 4.50
    })
    dias_desde_inicio = (df["data_coleta"] - pd.Timestamp("2023-01-01")).dt.days
    tendencia = dias_desde_inicio / 365 * 0.35  # sobe ~0.35 por ano
    ruido = rng.normal(0, 0.25, n_linhas)

    df["preco_venda"] = (preco_base + tendencia + ruido).round(2).clip(lower=2.5)

    return df
