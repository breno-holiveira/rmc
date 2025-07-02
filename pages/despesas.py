# pages/despesas.py

import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data(path="despesas_sp.xlsx"):
    df = pd.read_excel(path, parse_dates=["Ano"], dayfirst=True)
    df.columns = df.columns.str.strip()
    # Filtra anos de 2016 a 2021
    df = df[df["Ano"].dt.year.between(2016, 2021)]
    # Limpa strings
    for col in df.select_dtypes("object"):
        df[col] = df[col].str.strip()
    # Converte valores monetários
    df["Despesa"] = (
        df["Despesa"].astype(str)
        .str.replace(r"[R$.\s]", "", regex=True)
        .str.replace(",", ".", regex=False)
        .astype(float, errors="ignore")
    )
    df["Liquidado"] = (
        df["Liquidado"].astype(str)
        .str.replace(r"[R$.\s]", "", regex=True)
        .str.replace(",", ".", regex=False)
        .astype(float, errors="ignore")
    )
    return df

def show():
    st.markdown("## Despesas C&T (2016–2021)")

    df = load_data()
    if df.empty:
        st.warning("Nenhum dado disponível para 2016–2021.")
        return

    # Passo 1: Função 19
    df1 = df[df["Função"].str.startswith("19")]

    # Passo 2: Subfunções
    SUBFUN = ["571", "572", "573", "606", "664", "665"]
    df2 = df1[df1["Subfunção"].isin(SUBFUN)]

    # Passo 3: Palavras‑chave
    keywords = ["CIÊNCIA", "TECNOLOGIA", "PESQUISA", "DESENVOLVIMENTO", "INOVAÇÃO"]
    pattern = "|".join(keywords)
    mask = (
        df2["Programa"].str.upper().str.contains(pattern) |
        df2["Ação"].str.upper().str.contains(pattern) |
        df2["Funcional Programática"].str.upper().str.contains(pattern)
    )
    df3 = df2[mask]

    # Passo 4: Agregar e remover duplicatas
    df_ct = (
        pd.concat([df1, df2, df3])
        .drop_duplicates(subset=[
            "Ano", "Órgão", "UO", "Unidade Gestora",
            "Programa", "Ação", "Funcional Programática",
            "Credor", "Despesa", "Liquidado"
        ])
    )

    if df_ct.empty:
        st.warning("Nenhum registro de C&T encontrado.")
        return

    # Agregação por ano
    df_agg = df_ct.groupby(df_ct["Ano"].dt.year.rename("Ano")).agg(
        Total_Despesa=("Despesa", "sum"),
        Total_Liquidado=("Liquidado", "sum")
    ).reset_index()

    # Gráfico
    chart = (
        alt.Chart(df_agg)
        .mark_line(point=True)
        .encode(
            x="Ano:O",
            y=alt.Y("Total_Despesa:Q", title="Despesa (R$)"),
            tooltip=["Ano", "Total_Despesa"]
        )
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)

    # Detalhes
    with st.expander("Ver detalhes C&T"):
        st.dataframe(df_ct.reset_index(drop=True))
