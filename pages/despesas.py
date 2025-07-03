import streamlit as st
import pandas as pd
import unicodedata
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", sheet_name="despesas_sp")
    df.columns = df.columns.str.strip()
    
    # Trata os valores: remove espaços e converte para número (separador decimal é vírgula)
    df["Liquidado"] = (
        df["Liquidado"]
        .astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
    
    # Extrai o ano (mesmo que esteja como data textual tipo '31/12/2020')
    df["Ano"] = pd.to_datetime(df["Ano"], errors='coerce').dt.year
    return df

def normalizar(texto):
    if pd.isna(texto):
        return ""
    return unicodedata.normalize("NFKD", str(texto)).encode("ASCII", "ignore").decode("utf-8").lower()

def show():
    st.title("Análise de Despesas em Ciência e Tecnologia (C&T)")

    menu = st.radio("Selecione o tipo de despesa", ["Despesas estaduais em C&T", "Despesas municipais em C&T"])

    if menu == "Despesas estaduais em C&T":
        df = load_data()

        # Normalização
        df["Ação_norm"] = df["Ação"].apply(normalizar)
        df["Funcional_norm"] = df["Funcional Programática"].apply(normalizar)
        df["Credor_norm"] = df["Credor"].apply(normalizar)
        df["Despesa_norm"] = df["Despesa"].apply(normalizar)

        # Palavras para exclusão
        palavras_excluir = [
            "obras", "instalacoes", "mobiliario", "recreativo", "conservacao", "reformas",
            "reposicao", "despesas miudas", "auxilio", "seguro", "indenizacoes", "indenizacao",
            "ajuda de custo"
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

        df_filtrado = df[mask_funcao | mask_subfuncao | mask_keywords]

        st.markdown(f"**Registros encontrados:** `{len(df_filtrado)}`")

        # ---------- Gráfico 1: Total por Ano ----------
        st.subheader("Total Liquidado por Ano (R$)")
        dados_ano = df_filtrado.groupby("Ano")["Liquidado"].sum().reset_index()

        fig1, ax1 = plt.subplots()
        ax1.bar(dados_ano["Ano"].astype(str), dados_ano["Liquidado"] / 1e6)
        ax1.set_ylabel("Valor Liquidado (em milhões de R$)")
        ax1.set_xlabel("Ano")
        ax1.set_title("Total de Despesas em C&T por Ano")
        ax1.tick_params(axis='x', rotation=45)
        st.pyplot(fig1)

        # ---------- Gráfico 2: Por Unidade Gestora ----------
        st.subheader("Top 10 Unidades Gestoras por Valor Liquidado")
        dados_uo = df_filtrado.groupby("Unidade Gestora")["Liquidado"].sum().sort_values(ascending=False).head(10)

        fig2, ax2 = plt.subplots()
        ax2.barh(dados_uo.index[::-1], (dados_uo.values / 1e6)[::-1])
        ax2.set_xlabel("Valor Liquidado (em milhões de R$)")
        ax2.set_title("Top 10 Unidades Gestoras")
        st.pyplot(fig2)

        # ---------- Tabela com os dados filtrados ----------
        st.subheader("Tabela de dados filtrados")
        st.dataframe(df_filtrado[[
            "Ano", "Função", "Subfunção", "Programa", "Ação", "Despesa", "Credor",
            "Unidade Gestora", "Liquidado"
        ]], use_container_width=True)

    elif menu == "Despesas municipais em C&T":
        st.warning("Esta seção ainda será implementada.")

if __name__ == "__main__":
    show()
