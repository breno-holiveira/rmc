import streamlit as st
import pandas as pd
import unicodedata
import plotly.express as px

# === Carrega dados ===
@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", sheet_name="despesas_sp")
    df.columns = df.columns.str.strip()

    # Corrige valores sem separador de milhar e com vírgula decimal
    df["Liquidado"] = (
        df["Liquidado"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    df["Ano"] = df["Ano"].astype(str).str.extract(r"(\d{4})").astype(int)

    return df

# === Normalizador ===
def normalizar(texto):
    if pd.isna(texto):
        return ""
    return unicodedata.normalize("NFKD", str(texto)).encode("ASCII", "ignore").decode("utf-8").lower()

# === App principal ===
def show():
    st.title("Análise de Despesas em C&T – Campinas/SP")

    opcao = st.selectbox("Selecione o tipo de despesa", ["Despesas estaduais em C&T", "Despesas municipais em C&T"])

    if opcao == "Despesas municipais em C&T":
        st.info("Em breve: módulo de despesas municipais.")
        return

    df = load_data()

    # --- Normalização ---
    df["Ação_norm"] = df["Ação"].apply(normalizar)
    df["Funcional_norm"] = df["Funcional Programática"].apply(normalizar)
    df["Credor_norm"] = df["Credor"].apply(normalizar)
    df["Despesa_norm"] = df["Despesa"].apply(normalizar)

    # --- Exclusões específicas ---
    palavras_excluir = [
        "obras", "instalacoes", "mobiliario", "recreativo", "conservacao",
        "reformas", "reposicao", "despesas miudas", "auxilio", "seguro",
        "indenizacoes", "indenizacao", "ajuda de custo"
    ]
    mask_excluir = df["Despesa_norm"].str.contains("|".join(palavras_excluir), na=False)
    df = df[~mask_excluir]

    # --- Palavras-chave C&T ---
    keywords = [
        "pesquisa", "cientifica", "ciencia", "inovacao", "desenvolvimento",
        "p&d", "tecnologia", "academica", "robotica", "extensao"
    ]

    def contem_keywords(serie):
        return serie.str.contains("|".join(keywords), na=False)

    mask_keywords = (
        contem_keywords(df["Ação_norm"]) |
        contem_keywords(df["Funcional_norm"]) |
        contem_keywords(df["Credor_norm"]) |
        contem_keywords(df["Despesa_norm"])
    )

    # --- Filtros principais ---
    mask_funcao = df["Função"].astype(str).str.strip() == "19 - CIENCIA E TECNOLOGIA"

    subfuncoes_validas = [
        "571 - DESENVOLVIMENTO CIENTIFICO",
        "572 - DESENVOLVIMENTO TECNOLOGICO E ENGENHARIA",
        "573 - DIFUSAO DO CONHECIMENTO CIENT.E TECNOLOGICO",
        "606 - EXTENSAO RURAL",
        "665 - NORMALIZACAO E QUALIDADE"
    ]
    mask_subfuncao = df["Subfunção"].astype(str).str.strip().isin(subfuncoes_validas)

    # --- Aplicação dos filtros (OU) ---
    df_filtrado = df[mask_funcao | mask_subfuncao | mask_keywords]

    st.markdown(f"**Registros encontrados:** `{len(df_filtrado)}`")

    # === Gráfico 1: Total por Ano ===
    st.subheader("💰 Total Liquidado por Ano (R$ milhões)")

    dados_ano = df_filtrado.groupby("Ano")["Liquidado"].sum().reset_index()
    dados_ano["Liquidado (R$ milhões)"] = dados_ano["Liquidado"] / 1e6

    fig_ano = px.bar(
        dados_ano,
        x="Ano",
        y="Liquidado (R$ milhões)",
        labels={"Ano": "Ano", "Liquidado (R$ milhões)": "R$ milhões"},
        text_auto=".2s",
        color_discrete_sequence=["#4472c4"]
    )
    fig_ano.update_layout(yaxis_title="Valor (R$ milhões)", xaxis_title="Ano")
    st.plotly_chart(fig_ano, use_container_width=True)

    # === Gráfico 2: Unidades Gestoras ===
    st.subheader("🏛️ Top 10 Unidades Gestoras por Ano")

    anos_disponiveis = ["Todos"] + sorted(df_filtrado["Ano"].unique())
    ano_sel = st.selectbox("Filtrar por ano:", anos_disponiveis)

    if ano_sel != "Todos":
        df_uo = df_filtrado[df_filtrado["Ano"] == ano_sel]
    else:
        df_uo = df_filtrado.copy()

    dados_uo = df_uo.groupby("Unidade Gestora")["Liquidado"].sum().sort_values(ascending=False).head(10).reset_index()
    dados_uo["Valor (R$ milhões)"] = dados_uo["Liquidado"] / 1e6

    fig_uo = px.bar(
        dados_uo,
        x="Valor (R$ milhões)",
        y="Unidade Gestora",
        orientation="h",
        labels={"Valor (R$ milhões)": "R$ milhões", "Unidade Gestora": "UG"},
        text_auto=".2s",
        color_discrete_sequence=["#70ad47"]
    )
    fig_uo.update_layout(xaxis_title="Valor (R$ milhões)", yaxis_title="Unidade Gestora")
    st.plotly_chart(fig_uo, use_container_width=True)

    # === Tabela com dados ===
    with st.expander("📄 Ver dados filtrados"):
        st.dataframe(df_filtrado[[
            "Ano", "Programa", "Órgão", "UO", "Unidade Gestora", "Despesa", "Liquidado"
        ]], use_container_width=True)

if __name__ == "__main__":
    show()
