import streamlit as st
import pandas as pd
import unicodedata
import plotly.express as px

# === Carrega dados ===
@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", sheet_name="despesas_sp")
    df.columns = df.columns.str.strip()

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
    st.markdown("## Dispêndios públicos em C&T liquidados no município de Campinas")

    opcao = st.selectbox("Selecione o tipo de despesa", ["Despesas estaduais em C&T", "Despesas municipais em C&T"], key="tipo_despesa")

    if opcao == "Despesas municipais em C&T":
        st.info("Despesas municipais a serem inseridas...")
        return

    df = load_data()

    # Normalização
    df["Ação_norm"] = df["Ação"].apply(normalizar)
    df["Funcional_norm"] = df["Funcional Programática"].apply(normalizar)
    df["Credor_norm"] = df["Credor"].apply(normalizar)
    df["Despesa_norm"] = df["Despesa"].apply(normalizar)

    palavras_excluir = [
        "obras", "instalacoes", "mobiliario", "recreativo", "conservacao",
        "reformas", "reposicao", "despesas miudas", "auxilio", "seguro",
        "indenizacoes", "indenizacao", "ajuda de custo"
    ]
    mask_excluir = df["Despesa_norm"].str.contains("|".join(palavras_excluir), na=False)
    df = df[~mask_excluir]

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

    # === Novo Gráfico de Barras Agrupadas ===
    df_filtrado["Subfunção_Label"] = df_filtrado["Subfunção"].str.extract(r"\d+\s*-\s*(.*)", expand=False).fillna("Outros")

    dados_grouped = (
        df_filtrado.groupby(["Ano", "Subfunção_Label"])["Liquidado"]
        .sum()
        .reset_index()
    )

    fig_grouped = px.bar(
        dados_grouped,
        x="Ano",
        y="Liquidado",
        color="Subfunção_Label",
        barmode="group",
        labels={"Liquidado": "R$", "Ano": "Ano", "Subfunção_Label": "Categoria"},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_grouped.update_layout(
        title="Dispêndios liquidados por Subfunção e Ano (R$)",
        title_x=0.0,
        yaxis_title="Valor (R$)",
        xaxis_title="Ano",
        hovermode="x unified",
        legend_title="Subfunção",
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial")
    )
    fig_grouped.update_traces(
        hovertemplate="<b>Ano:</b> %{x}<br><b>Categoria:</b> %{legendgroup}<br><b>Valor:</b> R$ %{y:,.2f}<extra></extra>"
    )
    st.plotly_chart(fig_grouped, use_container_width=True)

    # === Tabela com dados ===
    with st.expander("📄 Visualizar os dados filtrados"):
        st.dataframe(df_filtrado[[ 
            "Ano", "Função", "Subfunção", "Ação", "Funcional Programática", "Credor", 
            "Despesa", "Programa", "Órgão", "UO", "Unidade Gestora", "Liquidado"
        ]], use_container_width=True)

if __name__ == "__main__":
    show()
