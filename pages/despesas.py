import streamlit as st
import pandas as pd
import unicodedata
import plotly.express as px

# === Carrega dados ===
@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", sheet_name="despesas_sp")
    df.columns = df.columns.str.strip()

    # Corrige valores numéricos
    df["Liquidado"] = (
        df["Liquidado"]
        .astype(str)
        .str.replace(",", ".", regex=False)  # vírgula decimal → ponto
        .astype(float)
    )

    df["Ano"] = df["Ano"].astype(str).str.extract(r"(\d{4})").astype(int)
    return df

# === Função para normalizar texto (acentos + caixa baixa) ===
def normalizar(texto):
    if pd.isna(texto):
        return ""
    return unicodedata.normalize("NFKD", str(texto)).encode("ASCII", "ignore").decode("utf-8").lower()

# === App principal ===
def show():
    st.title("📊 Análise de Despesas em C&T – Campinas/SP")

    # Caixa de seleção mais compacta
    opcao = st.selectbox(
        "Tipo de despesa:",
        ["Despesas estaduais em C&T", "Despesas municipais em C&T"],
        index=0
    )

    if opcao == "Despesas municipais em C&T":
        st.info("🔧 Em breve: módulo de despesas municipais.")
        return

    df = load_data()

    # Normalizar colunas para busca textual
    df["Ação_norm"] = df["Ação"].apply(normalizar)
    df["Funcional_norm"] = df["Funcional Programática"].apply(normalizar)
    df["Credor_norm"] = df["Credor"].apply(normalizar)
    df["Despesa_norm"] = df["Despesa"].apply(normalizar)

    # Filtro: excluir itens irrelevantes
    palavras_excluir = [
        "obras", "instalacoes", "mobiliario", "recreativo", "conservacao",
        "reformas", "reposicao", "despesas miudas", "auxilio", "seguro",
        "indenizacoes", "indenizacao", "ajuda de custo"
    ]
    df = df[~df["Despesa_norm"].str.contains("|".join(palavras_excluir), na=False)]

    # Palavras-chave para identificar C&T
    keywords = [
        "pesquisa", "cientifica", "ciencia", "inovacao", "desenvolvimento",
        "p&d", "tecnologia", "academica", "robotica", "extensao"
    ]

    def contem_keywords(serie):
        return serie.str.contains("|".join(keywords), na=False)

    # Máscaras
    mask_funcao = df["Função"].astype(str).str.strip() == "19 - CIENCIA E TECNOLOGIA"

    subfuncoes_validas = [
        "571 - DESENVOLVIMENTO CIENTIFICO",
        "572 - DESENVOLVIMENTO TECNOLOGICO E ENGENHARIA",
        "573 - DIFUSAO DO CONHECIMENTO CIENT.E TECNOLOGICO",
        "606 - EXTENSAO RURAL",
        "665 - NORMALIZACAO E QUALIDADE"
    ]
    mask_subfuncao = df["Subfunção"].astype(str).str.strip().isin(subfuncoes_validas)

    mask_keywords = (
        contem_keywords(df["Ação_norm"]) |
        contem_keywords(df["Funcional_norm"]) |
        contem_keywords(df["Credor_norm"]) |
        contem_keywords(df["Despesa_norm"])
    )

    # Aplicação final dos filtros (OU)
    df_filtrado = df[mask_funcao | mask_subfuncao | mask_keywords]

    st.markdown(f"**Registros encontrados:** `{len(df_filtrado)}`")

    # === Gráfico 1: Total por Ano ===
    st.subheader("💰 Total Liquidado por Ano")

    dados_ano = df_filtrado.groupby("Ano")["Liquidado"].sum().reset_index()

    fig_ano = px.bar(
        dados_ano,
        x="Ano",
        y="Liquidado",
        labels={"Liquidado": "Valor (R$)", "Ano": "Ano"},
        color_discrete_sequence=["#2a82d7"],
        text_auto=True
    )
    fig_ano.update_layout(
        yaxis_title="Valor Liquidado (R$)",
        xaxis_title="Ano",
        title_font_size=18,
        font=dict(family="Arial", size=13),
    )
    st.plotly_chart(fig_ano, use_container_width=True)

    # === Gráfico 2: Top Unidades Gestoras ===
    st.subheader("🏛️ Top 10 Unidades Gestoras")

    anos_disponiveis = ["Todos"] + sorted(df_filtrado["Ano"].unique())
    ano_sel = st.selectbox("Filtrar por ano:", anos_disponiveis, index=0)

    if ano_sel != "Todos":
        df_uo = df_filtrado[df_filtrado["Ano"] == ano_sel]
    else:
        df_uo = df_filtrado.copy()

    dados_uo = (
        df_uo.groupby("Unidade Gestora")["Liquidado"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_uo = px.bar(
        dados_uo,
        x="Liquidado",
        y="Unidade Gestora",
        orientation="h",
        labels={"Liquidado": "Valor (R$)", "Unidade Gestora": "UG"},
        color_discrete_sequence=["#00a65a"],
        text_auto=True
    )
    fig_uo.update_layout(
        xaxis_title="Valor Liquidado (R$)",
        yaxis_title="Unidade Gestora",
        title_font_size=18,
        font=dict(family="Arial", size=13),
    )
    st.plotly_chart(fig_uo, use_container_width=True)

    # === Tabela final ===
    with st.expander("📄 Ver dados filtrados"):
        st.dataframe(df_filtrado[[
            "Ano", "Programa", "Órgão", "UO", "Unidade Gestora", "Despesa", "Liquidado"
        ]], use_container_width=True)

if __name__ == "__main__":
    show()
