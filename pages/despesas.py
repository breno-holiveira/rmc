# pages/despesas.py

import streamlit as st
import pandas as pd

@st.cache_data
def load_data(path="despesas_sp.xlsx"):
    # Lê o Excel forçando engine openpyxl
    df = pd.read_excel(path, engine="openpyxl", parse_dates=["Ano"], dayfirst=True)
    # Remove espaços nos nomes de coluna
    df.columns = df.columns.str.strip()
    # Filtra anos fixos 2016–2021
    df = df[df["Ano"].dt.year.between(2016, 2021)]
    # Limpa strings de texto
    for col in df.select_dtypes("object"):
        df[col] = df[col].astype(str).str.strip()
    # Converte moeda para float, ignorando erros
    df["Despesa"] = (
        df["Despesa"]
        .astype(str)
        .str.replace(r"[R$.\s]", "", regex=True)
        .str.replace(",", ".", regex=False)
        .apply(lambda x: float(x) if x.replace(".","",1).isdigit() else None)
    )
    df["Liquidado"] = (
        df["Liquidado"]
        .astype(str)
        .str.replace(r"[R$.\s]", "", regex=True)
        .str.replace(",", ".", regex=False)
        .apply(lambda x: float(x) if x.replace(".","",1).isdigit() else None)
    )
    # Descartar linhas sem valor em Despesa
    return df.dropna(subset=["Despesa"])

def show():
    st.title("Despesas C&T (2016–2021)")

    df = load_data()
    if df.empty:
        st.warning("Nenhum dado disponível para 2016–2021.")
        return

    # 1) Filtra Função 19
    df1 = df[df["Função"].str.startswith("19", na=False)]

    # 2) Filtra Subfunções
    subfuncoes_ct = ["571", "572", "573", "606", "664", "665"]
    df2 = df1[df1["Subfunção"].isin(subfuncoes_ct)]

    # 3) Filtra por palavras-chave
    keywords = ["CIÊNCIA", "TECNOLOGIA", "PESQUISA", "DESENVOLVIMENTO", "INOVAÇÃO"]
    pattern = "|".join(keywords)
    mask = (
        df2["Programa"].str.upper().str.contains(pattern, na=False) |
        df2["Ação"].str.upper().str.contains(pattern, na=False) |
        df2["Funcional Programática"].str.upper().str.contains(pattern, na=False)
    )
    df3 = df2[mask]

    # 4) Consolida e remove duplicatas
    df_ct = pd.concat([df1, df2, df3], ignore_index=True)
    df_ct = df_ct.drop_duplicates(subset=[
        "Ano", "Órgão", "UO", "Unidade Gestora",
        "Programa", "Ação", "Funcional Programática",
        "Credor", "Despesa", "Liquidado"
    ])

    if df_ct.empty:
        st.warning("Nenhum registro de C&T encontrado.")
        return

    # Mostra o resultado final
    st.subheader("Total de registros filtrados")
    st.write(len(df_ct))
    st.subheader("Resumo de Valores")
    st.write(df_ct[["Despesa", "Liquidado"]].sum().rename({"Despesa":"Total Despesa","Liquidado":"Total Liquidado"}))

    with st.expander("Ver dados detalhados"):
        st.dataframe(df_ct.reset_index(drop=True), use_container_width=True)
