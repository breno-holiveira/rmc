import streamlit as st
import pandas as pd
import unicodedata
import matplotlib.pyplot as plt

# === Carregamento de dados ===
@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", sheet_name="despesas_sp")
    df.columns = df.columns.str.strip()

    # Corrige valores com vírgula decimal e sem separador de milhar
    df["Liquidado"] = (
        df["Liquidado"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    # Extrai o ano da coluna (assumindo datas como texto '31/12/2016', etc)
    df["Ano"] = df["Ano"].astype(str).str.extract(r"(\d{4})").astype(int)

    return df

# === Função para normalizar texto ===
def normalizar(texto):
    if pd.isna(texto):
        return ""
    return unicodedata.normalize("NFKD", str(texto)).encode("ASCII", "ignore").decode("utf-8").lower()

# === Aplicação ===
def show():
    st.title("Análise de Despesas em C&T – Campinas/SP")

    opcao = st.selectbox("Selecione o tipo de despesa", ["Despesas estaduais em C&T", "Despesas municipais em C&T"])

    if opcao == "Despesas municipais em C&T":
        st.info("Em breve: módulo de despesas municipais.")
        return

    df = load_data()

    # --- Normalizar colunas-alvo ---
    df["Ação_norm"] = df["Ação"].apply(normalizar)
    df["Funcional_norm"] = df["Funcional Programática"].apply(normalizar)
    df["Credor_norm"] = df["Credor"].apply(normalizar)
    df["Despesa_norm"] = df["Despesa"].apply(normalizar)

    # --- Exclusão por palavras proibidas ---
    palavras_excluir = [
        "obras", "instalacoes", "mobiliario", "recreativo", "conservacao",
        "reformas", "reposicao", "despesas miudas", "auxilio", "seguro",
        "indenizacoes", "indenizacao", "ajuda de custo"
    ]
    mask_excluir = df["Despesa_norm"].str.contains("|".join(palavras_excluir), na=False)
    df = df[~mask_excluir]

    # --- Palavras-chave de C&T ---
    keywords = [
        "pesquisa", "cientifica", "ciencia", "inovacao", "desenvolvimento",
        "p&d", "tecnologia", "academica", "robotica", "extensao",
    ]

    def contem_keywords(serie):
        return serie.str.contains("|".join(keywords), na=False)

    mask_keywords = (
        contem_keywords(df["Ação_norm"]) |
        contem_keywords(df["Funcional_norm"]) |
        contem_keywords(df["Credor_norm"]) |
        contem_keywords(df["Despesa_norm"])
    )

    # --- Filtros por função e subfunções ---
    mask_funcao = df["Função"].astype(str).str.strip() == "19 - CIENCIA E TECNOLOGIA"

    subfuncoes_validas = [
        "571 - DESENVOLVIMENTO CIENTIFICO",
        "572 - DESENVOLVIMENTO TECNOLOGICO E ENGENHARIA",
        "573 - DIFUSAO DO CONHECIMENTO CIENT.E TECNOLOGICO",
        "606 - EXTENSAO RURAL",
        "665 - NORMALIZACAO E QUALIDADE"
    ]
    mask_subfuncao = df["Subfunção"].astype(str).str.strip().isin(subfuncoes_validas)

    # --- Aplica filtro (OU) ---
    df_filtrado = df[mask_funcao | mask_subfuncao | mask_keywords]

    st.markdown(f"**Registros encontrados:** `{len(df_filtrado)}`")

    # === Gráfico 1: Total por Ano ===
    st.subheader("Total Liquidado por Ano (R$)")
    dados_ano = df_filtrado.groupby("Ano")["Liquidado"].sum().reset_index()

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.bar(dados_ano["Ano"], dados_ano["Liquidado"] / 1e6, color="#4472c4")
    ax1.set_title("Despesas Totais em C&T por Ano")
    ax1.set_ylabel("Valor Liquidado (em milhões R$)")
    ax1.set_xlabel("Ano")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)
    st.pyplot(fig1)

    # === Gráfico 2: Top Unidades Gestoras ===
    st.subheader("Unidades Gestoras com Maior Valor Liquidado")
    anos_disponiveis = ["Todos"] + sorted(df_filtrado["Ano"].unique().tolist())
    ano_sel = st.selectbox("Filtrar por ano:", anos_disponiveis)

    if ano_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Ano"] == ano_sel]

    dados_uo = df_filtrado.groupby("Unidade Gestora")["Liquidado"].sum().sort_values(ascending=False).head(10)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.barh(dados_uo.index[::-1], dados_uo.values[::-1] / 1e6, color="#70ad47")
    ax2.set_title("Top 10 Unidades Gestoras")
    ax2.set_xlabel("Valor Liquidado (em milhões R$)")
    ax2.grid(axis="x", linestyle="--", alpha=0.5)
    st.pyplot(fig2)

    # === Tabela final ===
    with st.expander("Ver dados filtrados"):
        st.dataframe(df_filtrado[[
            "Ano", "Programa", "Órgão", "UO", "Unidade Gestora", "Despesa", "Liquidado"
        ]], use_container_width=True)

if __name__ == "__main__":
    show()
