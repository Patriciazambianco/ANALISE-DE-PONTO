import streamlit as st
import pandas as pd
import gdown

st.set_page_config("Relatório de Ponto", layout="wide")
st.title("📊 Dashboard de Ponto")

# Baixar arquivo do Google Drive
file_id = "1HnJtt5c-7qdhzVTe5vo_a8o05exI5ETF"
url = f"https://drive.google.com/uc?id={file_id}"
output = "dados.xlsx"
gdown.download(url, output, quiet=False)

# Leitura
df = pd.read_excel(output)

# Conversão de colunas para hora
df['Ponto Inicial'] = pd.to_datetime(df['Ponto Inicial'], errors='coerce').dt.time
df['Ponto Final'] = pd.to_datetime(df['Ponto Final'], errors='coerce').dt.time
df['JORNADA.ENTRADA'] = pd.to_datetime(df['JORNADA.ENTRADA'], errors='coerce').dt.time
df['JORNADA.SAIDA'] = pd.to_datetime(df['JORNADA.SAIDA'], errors='coerce').dt.time

# Funções auxiliares
def fora_jornada(row):
    try:
        if row['Ponto Inicial'] and row['JORNADA.ENTRADA'] and row['Ponto Inicial'] < row['JORNADA.ENTRADA']:
            return True
        if row['Ponto Final'] and row['JORNADA.SAIDA'] and row['Ponto Final'] > row['JORNADA.SAIDA']:
            return True
        return False
    except:
        return False

def hora_extra(row):
    try:
        if row['Ponto Final'] and row['JORNADA.SAIDA'] and row['Ponto Final'] > row['JORNADA.SAIDA']:
            return True
        return False
    except:
        return False

# Aplica lógica
df['Fora da Jornada'] = df.apply(fora_jornada, axis=1)
df['Hora Extra'] = df.apply(hora_extra, axis=1)

# Agrupamentos
fora_df = df[df['Fora da Jornada']]
extra_df = df[df['Hora Extra']]

# KPIs
col1, col2 = st.columns(2)
col1.metric("👟 Funcionários Fora da Jornada", fora_df['Funcionario'].nunique())
col2.metric("⏱️ Funcionários com Hora Extra", extra_df['Funcionario'].nunique())

# Tabelas detalhadas
with st.expander("🔍 Detalhe: Batidas Fora da Jornada"):
    st.dataframe(fora_df[['Funcionario', 'Data', 'Ponto Inicial', 'Ponto Final', 'JORNADA.ENTRADA', 'JORNADA.SAIDA']])

with st.expander("🔍 Detalhe: Dias com Hora Extra"):
    st.dataframe(extra_df[['Funcionario', 'Data', 'Ponto Final', 'JORNADA.SAIDA']])


