import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    xls = pd.ExcelFile("despesas_sp.xlsx")
    st.write("Abas disponíveis no arquivo:", xls.sheet_names)  # Mostra as abas no app
    df = xls.parse(xls.sheet_names[0])  # Lê a primeira aba
    return df
