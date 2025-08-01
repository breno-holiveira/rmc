import streamlit as st
import pandas as pd
import unicodedata
import plotly.express as px

st.markdown('## Dispêndios Estaduais em C&T')

# === Carrega dados ===
@st.cache_data
def load_data():
    df = pd.read_csv("arquivos/despesas_sp.csv", encoding="latin1")
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

# === Função para normalizar strings ===
def normalizar(texto):
    if pd.isna(texto):
        return ""
    return unicodedata.normalize("NFKD", str(texto)).encode("ASCII", "ignore").decode("utf-8").lower()

# === App principal ===
def show():
    st.markdown("## Dispêndios públicos em C&T liquidados no município de Campinas")

    opcao = st.selectbox("Selecione o tipo de despesa", ["Despesas estaduais em C&T", "Despesas municipais em C&T"], key="tipo_despesa")

    if opcao == "Despesas municipais em C&T":
        st.info("Despesas municipais a serem inseridas...")
        return

    df = load_data()

    # Normalizações
    df["Ação_norm"] = df["Ação"].apply(normalizar)
    df["Funcional_norm"] = df["Funcional Programática"].apply(normalizar)
    df["Credor_norm"] = df["Credor"].apply(normalizar)
    df["Despesa_norm"] = df["Despesa"].apply(normalizar)

    # Filtragem: exclusões específicas
    palavras_excluir = [
        "obras", "instalacoes", "mobiliario", "recreativo", "conservacao",
        "reformas", "reposicao", "despesas miudas", "auxilio", "seguro",
        "indenizacoes", "indenizacao", "ajuda de custo"
    ]
    mask_excluir = df["Despesa_norm"].str.contains("|".join(palavras_excluir), na=False)
    df = df[~mask_excluir]

    # Palavras-chave C&T
    keywords = [
        "pesquisa", "cientifica", "ciencia", "inovacao", "desenvolvimento",
        "p&d", "tecnologia", "academica", "robotica", "extensao"
    ]
    def contem_keywords(serie):
        return serie.str.contains("|".join(keywords), na=False)

    mask_keywords = (
        contem_keywords(df["Ação_norm"]) |
        contem_keywords(df["Funcional_norm"]) |
        contem_keywords(df["Despesa_norm"])
    )

    mask_funcao = df["Função"].astype(str).str.strip() == "19 - CIENCIA E TECNOLOGIA"
    subfuncoes_validas = [
        "571 - DESENVOLVIMENTO CIENTIFICO",
        "572 - DESENVOLVIMENTO TECNOLOGICO E ENGENHARIA",
        "573 - DIFUSAO DO CONHECIMENTO CIENT.E TECNOLOGICO",
        "606 - EXTENSAO RURAL",
        "665 - NORMALIZACAO E QUALIDADE"
    ]
    mask_subfuncao = df["Subfunção"].astype(str).str.strip().isin(subfuncoes_validas)

    df_filtrado = df[mask_funcao | mask_subfuncao | mask_keywords]

    st.markdown(f"**Registros encontrados:** {len(df_filtrado)}")
    st.markdown('***')

    # === Gráfico 1: Total por Ano ===
    dados_ano = df_filtrado.groupby("Ano")["Liquidado"].sum().reset_index()
    fig_ano = px.bar(
        dados_ano,
        x="Ano",
        y="Liquidado",
        labels={"Ano": "Ano", "Liquidado": "R$"},
        color_discrete_sequence=["#4472c4"]
    )
    fig_ano.update_layout(
        yaxis_title="Valor (R$)",
        xaxis_title="Ano",
        title="Valor total liquidado por ano (R$)",
        title_x=0.0,
        hovermode="closest",
        hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial")
    )
    fig_ano.update_traces(hovertemplate="<b>Ano:</b> %{x}<br><b>Valor:</b> R$ %{y:,.2f}<extra></extra>")
    st.plotly_chart(fig_ano, use_container_width=True)

    # === Gráfico 2: Unidades Gestoras ===
    anos_disponiveis = ["Todos"] + sorted(df_filtrado["Ano"].unique())
    ano_sel = st.selectbox("Filtrar por ano:", anos_disponiveis, key="ano_selecionado")

    if ano_sel != "Todos":
        df_uo = df_filtrado[df_filtrado["Ano"] == ano_sel]
    else:
        df_uo = df_filtrado.copy()

    dados_uo = (
        df_uo.groupby("Unidade Gestora")["Liquidado"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .iloc[::-1]
        .reset_index()
    )

    fig_uo = px.bar(
        dados_uo,
        x="Liquidado",
        y="Unidade Gestora",
        orientation="h",
        labels={"Liquidado": "R$", "Unidade Gestora": "UG"},
        color_discrete_sequence=["#70ad47"]
    )
    fig_uo.update_layout(
        xaxis_title="Valor (R$)",
        yaxis_title="Unidade Gestora",
        title="Valor por unidade gestora (R$)",
        title_x=0.0,
        hovermode="closest",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )
    fig_uo.update_traces(hovertemplate="<b>Unidade Gestora:</b> %{y}<br><b>Valor:</b> R$ %{x:,.2f}<extra></extra>")
    st.plotly_chart(fig_uo, use_container_width=True)

    # === Tabela final ===
    with st.expander("📄 Visualizar os dados filtrados"):
        st.dataframe(df_filtrado[[
            "Ano", "Função", "Subfunção", "Ação", "Funcional Programática", 
            "Credor", "Despesa", "Programa", "Órgão", "UO", 
            "Unidade Gestora", "Liquidado"
        ]], use_container_width=True)

if __name__ == "__main__":
    show()
