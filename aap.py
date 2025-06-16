import streamlit as st
import pandas as pd
import gdown
from io import BytesIO

st.set_page_config("Relatório de Ponto", layout="wide")
st.title("📊 Dashboard de Ponto")

# 🔄 Cache de carregamento
@st.cache_data
def carregar_dados():
    file_id = "1HnJtt5c-7qdhzVTe5vo_a8o05exI5ETF"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "dados.xlsx"
    gdown.download(url, output, quiet=False)
    df = pd.read_excel(output)
    return df

df = carregar_dados()

# 📆 Conversão de horários
df['Ponto Inicial'] = pd.to_datetime(df['Ponto Inicial'], errors='coerce').dt.time
df['Ponto Final'] = pd.to_datetime(df['Ponto Final'], errors='coerce').dt.time
df['JORNADA.ENTRADA'] = pd.to_datetime(df['JORNADA.ENTRADA'], errors='coerce').dt.time
df['JORNADA.SAIDA'] = pd.to_datetime(df['JORNADA.SAIDA'], errors='coerce').dt.time

# 📋 Lógicas
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

df['Fora da Jornada'] = df.apply(fora_jornada, axis=1)
df['Hora Extra'] = df.apply(hora_extra, axis=1)

fora_df = df[df['Fora da Jornada']]
extra_df = df[df['Hora Extra']]

# 📊 KPIs
col1, col2 = st.columns(2)
col1.metric("👟 Funcionários Fora da Jornada", fora_df['Funcionario'].nunique())
col2.metric("⏱️ Funcionários com Hora Extra", extra_df['Funcionario'].nunique())

# 📥 Botões de download protegidos
def gerar_excel(df):
    output = BytesIO()
    df.to_excel(output, index=False)
    return output.getvalue()

# 🔍 Fora da Jornada
with st.expander("🔍 Detalhe: Fora da Jornada"):
    if not fora_df.empty:
        st.dataframe(fora_df[['Funcionario', 'Data', 'Ponto Inicial', 'Ponto Final', 'JORNADA.ENTRADA', 'JORNADA.SAIDA']])
        st.download_button("📥 Baixar Fora da Jornada", gerar_excel(fora_df), file_name="fora_da_jornada.xlsx")
    else:
        st.info("Nenhum registro fora da jornada encontrado.")

# 🔍 Hora Extra
with st.expander("🔍 Detalhe: Hora Extra"):
    if not extra_df.empty:
        st.dataframe(extra_df[['Funcionario', 'Data', 'Ponto Final', 'JORNADA.SAIDA']])
        st.download_button("📥 Baixar Hora Extra", gerar_excel(extra_df), file_name="hora_extra.xlsx")
    else:
        st.info("Nenhum registro de hora extra encontrado.")
