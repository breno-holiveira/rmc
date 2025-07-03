import streamlit as st
import pandas as pd
import unicodedata

@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", sheet_name="despesas_sp")
    df.columns = df.columns.str.strip()

    # Corrigir valores da coluna 'Liquidado'
    # Se os valores estiverem como: 383267,93 (vírgula decimal, sem milhar), apenas troca vírgula por ponto
    df["Liquidado"] = df["Liquidado"].astype(str).str.replace(",", ".", regex=False)
    df["Liquidado"] = pd.to_numeric(df["Liquidado"], errors='coerce')

    return df

# Remove acentos e converte para minúsculas
def normalizar(texto):
    if pd.isna(texto):
        return ""
    return unicodedata.normalize("NFKD", str(texto)).encode("ASCII", "ignore").decode("utf-8").lower()

def show():
    st.title("Filtro: Função 19, Subfunções específicas OU Palavras-chave em colunas (excluindo termos específicos)")

    df = load_data()

    # --- Normalizar colunas-alvo ---
    df["Ação_norm"] = df["Ação"].apply(normalizar)
    df["Funcional_norm"] = df["Funcional Programática"].apply(normalizar)
    df["Credor_norm"] = df["Credor"].apply(normalizar)
    df["Despesa_norm"] = df["Despesa"].apply(normalizar)

    # --- Excluir linhas com palavras proibidas na coluna Despesa ---
    palavras_excluir = [
        "obras", "instalacoes", "mobiliario", "recreativo", "conservacao",
        "reformas", "reposicao", "despesas miudas", "auxilio", "seguro",
        "indenizacoes", "indenizacao", "ajuda de custo"
    ]
    mask_excluir = df["Despesa_norm"].str.contains("|".join(palavras_excluir), na=False)
    df = df[~mask_excluir]

    # --- Palavras-chave relacionadas a C&T ---
    keywords = [
        "pesquisa", "cientifica", "ciencia", "inovacao", "desenvolvimento",
        "p&d", "tecnologia", "academica", "robotica", "extensao"
    ]

    # --- Máscaras principais ---
    mask_funcao = df["Função"].astype(str).str.strip() == "19 - CIENCIA E TECNOLOGIA"

    subfuncoes_validas = [
        "571 - DESENVOLVIMENTO CIENTIFICO",
        "572 - DESENVOLVIMENTO TECNOLOGICO E ENGENHARIA",
        "573 - DIFUSAO DO CONHECIMENTO CIENT.E TECNOLOGICO",
        "606 - EXTENSAO RURAL",
        "665 - NORMALIZACAO E QUALIDADE"
    ]
    mask_subfuncao = df["Subfunção"].astype(str).str.strip().isin(subfuncoes_validas)

    def contem_keywords(serie):
        return serie.str.contains("|".join(keywords), na=False)

    mask_keywords = (
        contem_keywords(df["Ação_norm"]) |
        contem_keywords(df["Funcional_norm"]) |
        contem_keywords(df["Credor_norm"]) |
        contem_keywords(df["Despesa_norm"])
    )

    # --- Aplica filtro combinado (OU) ---
    df_filtrado = df[mask_funcao | mask_subfuncao | mask_keywords]

    # --- Exibe resultado ---
    st.markdown(f"**Registros encontrados:** `{len(df_filtrado)}`")
    st.dataframe(df_filtrado, use_container_width=True)

    # --- Gráfico por ano ---
    try:
        df_filtrado["Ano"] = pd.to_datetime(df_filtrado["Ano"], errors='coerce').dt.year
        gastos_ano = df_filtrado.groupby("Ano")["Liquidado"].sum().reset_index()
        st.subheader("Total de despesas por ano")
        st.bar_chart(gastos_ano.set_index("Ano")["Liquidado"])
    except:
        st.warning("Não foi possível gerar o gráfico por ano.")

    # --- Gráfico por unidade gestora ---
    try:
        top_ug = df_filtrado.groupby("Unidade Gestora")["Liquidado"].sum().nlargest(10).reset_index()
        st.subheader("Top 10 unidades gestoras por despesa")
        st.bar_chart(top_ug.set_index("Unidade Gestora")["Liquidado"])
    except:
        st.warning("Não foi possível gerar o gráfico por unidade gestora.")

if __name__ == "__main__":
    show()
