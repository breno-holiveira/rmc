import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", dtype=str)

    # Corrige nomes das colunas
    df.columns = df.columns.str.strip()

    # Conversão da coluna "Ano" para inteiro
    df["Ano"] = pd.to_datetime(df["Ano"], errors="coerce").dt.year

    # Limpa e converte valores da coluna "Liquidado"
    df["Liquidado"] = (
        df["Liquidado"]
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
        .astype(float)
    )

    return df

def show():
    st.markdown("## Análise de Despesas em C&T (2016–2021)")

    df = load_data()

    # Filtro por anos válidos
    df = df[df["Ano"].between(2016, 2021)]

    # Filtra Função 19 - Ciência e Tecnologia
    funcao_ct = df[df["Função"].str.startswith("19")]

    # Subfunções reconhecidas como C&T
    subfuncoes_ct = ["571", "572", "573", "606", "664", "665"]
    subfuncao_ct = df[df["Subfunção"].str.strip().str[:3].isin(subfuncoes_ct)]

    # Palavras-chave associadas à C&T
    palavras_ct = ["ciência", "cient", "tecnologia", "tecnológ", "inovação", "pesquisa", "C&T"]
    padrao = "|".join(palavras_ct)

    # Busca por palavras-chave nas colunas relacionadas
    por_palavras = df[
        df["Programa"].str.lower().str.contains(padrao, na=False)
        | df["Ação"].str.lower().str.contains(padrao, na=False)
        | df["Funcional Programática"].str.lower().str.contains(padrao, na=False)
    ]

    # Concatena todos os resultados de C&T
    df_ct = pd.concat([funcao_ct, subfuncao_ct, por_palavras], ignore_index=True)

    # Remove duplicatas para evitar dupla contagem
    df_ct = df_ct.drop_duplicates()

    # Agregação por ano
    resumo = df_ct.groupby("Ano")["Liquidado"].sum().reset_index()

    # Gráfico de barras com totais por ano
    st.bar_chart(resumo.set_index("Ano"))

    # Exibição dos dados filtrados (opcional)
    with st.expander("Ver dados detalhados"):
        st.dataframe(df_ct)

