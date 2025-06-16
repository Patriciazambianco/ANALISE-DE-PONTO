import streamlit as st
import pandas as pd
import gdown

st.title("Análise de Ponto com Google Drive")

# Insira seu ID aqui 👇
file_id = "1HnJtt5c-7qdhzVTe5vo_a8o05exI5ETF"
url = f"https://drive.google.com/uc?id={file_id}"
output = "arquivo.xlsx"

# Baixar arquivo do Google Drive
try:
    gdown.download(url, output, quiet=False)
    df = pd.read_excel(output)
    st.success("Arquivo carregado com sucesso!")

    st.subheader("Visualização dos dados")
    st.dataframe(df)
    st.write(f"Total de registros: {len(df)}")

except Exception as e:
    st.error(f"Erro ao carregar: {e}")
