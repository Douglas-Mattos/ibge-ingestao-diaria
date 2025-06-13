import requests
import pandas as pd
import sqlite3
from datetime import date
import os

# 🔁 Etapa 1: Coletar dados da API IBGE
def coletar_estados_ibge():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    resposta = requests.get(url)
    dados = resposta.json()
    df = pd.DataFrame(dados)
    df['data_coleta'] = date.today().isoformat()
    return df[['id', 'sigla', 'nome', 'data_coleta']] 

# 🔁 Etapa 2: Salvar CSV local
df = coletar_estados_ibge()
arquivo_csv = f"ibge_estados_{date.today().isoformat()}.csv"
df.to_csv(arquivo_csv, index=False)
print("✔️ CSV gerado com sucesso:", arquivo_csv)

# 🔁 Etapa 3: Gravar no SQLite local
caminho_banco = "ibge.db"
conn = sqlite3.connect(caminho_banco)
df.to_sql("estados", conn, if_exists="replace", index=False)
conn.close()
print("✔️ Tabela 'estados' gravada com sucesso no SQLite.")
