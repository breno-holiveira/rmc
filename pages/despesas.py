# pages/despesas.py

import streamlit as st
import pandas as pd

@st.cache_data
def load_data(path="despesas_sp.xlsx"):
    df = pd.read_excel(path, engine="openpyxl")

    # Corrige nomes de colunas
    df.columns = df.columns.str.strip()

    # Converte 'Ano' para datetime (mesmo que só tenha ano no valor)
    df["Ano"] = pd.to_datetime(df["Ano"], dayfirst=True, errors="coerce")

    # Mantém apenas anos entre 2016 e 2021
    df = df[df["Ano"].dt.year.between(2016, 2021)]

    # Limpa campos monetários
    for campo in ["Despesa", "Liquidado"]:
        df[campo] = (
            df[campo]
            .astype(str)
            .str.replace(r"[R$.\s]", "", regex=True)
            .str.replace(",", ".", regex=False)
            .apply(pd.to_numeric, errors="coerce")
        )

    # Remove nulos de valor
    return df.dropna(subset=["Despesa"])

def show():
    st.title("Análise de Despesas em C&T (2016–2021)")

    df = load_data()
    if df.empty:
        st.warning("Base vazia após leitura.")
        return

    # Critério 1: Função 19 - Ciência e Tecnologia
    filtro_funcao = df["Função"].astype(str).str.startswith("19", na=False)
    df_funcao = df[filtro_funcao]

    # Critério 2: Subfunções relevantes
    subfun_ct = ["571", "572", "573", "606", "664", "665"]
    filtro_subfuncao = df["Subfunção"].astype(str).isin(subfun_ct)
    df_subfuncao = df[filtro_subfuncao]

    # Critério 3: palavras-chave nos programas/ações/funções programáticas
    palavras_chave = ["CIÊNCIA", "TECNOLOGIA", "PESQUISA", "INOVAÇÃO", "DESENVOLVIMENTO"]
    pattern = "|".join(palavras_chave)

    filtro_keywords = (
        df["Programa"].astype(str).str.upper().str.contains(pattern, na=False) |
        df["Ação"].astype(str).str.upper().str.contains(pattern, na=False) |
        df["Funcional Programática"].astype(str).str.upper().str.contains(pattern, na=False)
    )
    df_keywords = df[filtro_keywords]

    # Concatena tudo e remove duplicações
    df_ct = pd.concat([df_funcao, df_subfuncao, df_keywords], ignore_index=True)
    df_ct = df_ct.drop_duplicates()

    # Resultado final
    if df_ct.empty:
        st.error("Nenhuma despesa relacionada a C&T foi encontrada.")
        return

    st.subheader("Resumo de Despesas em Ciência e Tecnologia")
    st.write(f"Total de registros únicos: {len(df_ct)}")

    st.write("**Totais (R$)**")
    st.dataframe(
        df_ct[["Despesa", "Liquidado"]].sum().rename({"Despesa": "Total Empenhado", "Liquidado": "Total Liquidado"}).to_frame("Valor R$")
    )

    st.subheader("Tabela com as despesas filtradas")
    st.dataframe(df_ct.reset_index(drop=True), use_container_width=True)
