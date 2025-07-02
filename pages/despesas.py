import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", sheet_name="despesas_sp")

    # Corrigir nomes de colunas
    df.columns = df.columns.str.strip()

    # Extrair ano como inteiro
    df["Ano"] = df["Ano"].astype(str).str.extract(r"(\d{4})").astype(int)

    # Converter "Liquidado" para float
    df["Liquidado"] = (
        df["Liquidado"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    return df

def show():
    st.title("Análise de Despesas em C&T (2016–2021)")

    df = load_data()

    # --- Critérios de inclusão (OU) ---
    subfun_ct = ["571", "572", "573", "606", "664", "665"]
    keywords = [
        "pesquisa", "científica", "cientifica", "ciencia", "inovacao", "desenvolvimento",
        "P&D", "tecnologia", "laboratório", "laboratorio", "inovação", "técnico", "tecnico", "ciência"
        "tecnológico", "tecnologico", "formação", "formacao"
    ]

    # Máscaras individuais
    mask_func = df["Função"].astype(str).str.strip() == "19"
    mask_subfunc = df["Subfunção"].astype(str).isin(subfun_ct)

    def keyword_mask(col):
        return col.astype(str).str.lower().str.contains('|'.join(keywords), na=False)

    mask_keywords = (
        keyword_mask(df["Programa"]) |
        keyword_mask(df["Ação"]) |
        keyword_mask(df["Despesa"])
    )

    # Combina os três com OU
    df = df[mask_func | mask_subfunc | mask_keywords]

    # --- Exclusão de termos que não têm relação com C&T ---
    excluir = ["inativos", "pensionistas", "juros", "amortização", "assistencia hospitalar"]
    mask_excluir = df["Despesa"].astype(str).str.lower().str.contains('|'.join(excluir), na=False)
    df = df[~mask_excluir]

    # --- Filtro interativo por município ---
    municipios = sorted(df["Município"].dropna().unique())
    municipio_sel = st.selectbox(
        "Selecione o município",
        municipios,
        index=municipios.index("CAMPINAS") if "CAMPINAS" in municipios else 0
    )
    df = df[df["Município"] == municipio_sel]

    st.markdown(f"**Total de registros encontrados:** `{len(df)}`")

    # --- Gráfico 1: Evolução anual ---
    graf = df.groupby("Ano")["Liquidado"].sum().reset_index()

    fig = px.bar(
        graf,
        x="Ano",
        y="Liquidado",
        text_auto=".2s",
        labels={"Liquidado": "Valor Liquidado (R$)"},
        title=f"Dispêndios Públicos em C&T – {municipio_sel}",
    )
    fig.update_layout(
        yaxis_tickprefix="R$ ",
        xaxis_title="Ano",
        yaxis_title="Total Liquidado",
        title_x=0.05
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Gráfico 2: Programas ---
    graf2 = df.groupby(["Ano", "Programa"])["Liquidado"].sum().reset_index()

    fig2 = px.bar(
        graf2,
        x="Ano",
        y="Liquidado",
        color="Programa",
        labels={"Liquidado": "Valor Liquidado (R$)"},
        title=f"Programas de C&T em {municipio_sel}",
    )
    fig2.update_layout(
        yaxis_tickprefix="R$ ",
        xaxis_title="Ano",
        yaxis_title="Total por Programa",
        title_x=0.05
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Tabela de dados filtrados ---
    with st.expander("Ver dados brutos filtrados"):
        st.dataframe(df.reset_index(drop=True), use_container_width=True)
