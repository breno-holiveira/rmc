import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_excel("despesas_sp.xlsx", sheet_name="despesas_sp")

    # Corrigir nomes de colunas, se necessário
    df.columns = df.columns.str.strip()

    # Garantir que o ano seja inteiro
    df["Ano"] = df["Ano"].astype(str).str.extract(r"(\d{4})").astype(int)

    # Corrigir valor da coluna "Liquidado" (de string para float)
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

    # Filtro de ano
    df = df[(df["Ano"] >= 2016) & (df["Ano"] <= 2021)]

    # Códigos das Subfunções relacionadas a C&T segundo o RIECTI
    subfun_ct = ["571", "572", "573", "606", "664", "665"]
    func_ct = ["19"]  # Função Ciência e Tecnologia

    # Filtros por função e subfunção
    mask_func = df["Função"].astype(str).str.startswith(tuple(func_ct))
    mask_subfunc = df["Subfunção"].astype(str).isin(subfun_ct)
    df = df[mask_func | mask_subfunc]

    # Dicionário de palavras-chave relacionadas à C&T
    keywords = [
        "pesquisa", "científica", "cientifico", "desenvolvimento",
        "tecnologia", "laboratório", "inovação", "ciência", "técnico",
        "tecnológico", "formação", "universidade", "ensino", "acadêmica"
    ]

    # Filtros por palavras-chave
    def keyword_mask(col):
        return col.astype(str).str.lower().str.contains('|'.join(keywords), na=False)

    df = df[keyword_mask(df["Programa"]) | keyword_mask(df["Ação"]) | keyword_mask(df["Despesa"])]

    # Excluir termos explícitos que não representam C&T
    excluir = ["inativos", "pensionistas", "previdência", "juros", "amortização"]
    mask_excluir = df["Despesa"].astype(str).str.lower().str.contains('|'.join(excluir), na=False)
    df = df[~mask_excluir]

    # Filtro interativo por município
    municipios = sorted(df["Município"].dropna().unique())
    municipio_sel = st.selectbox("Selecione o município", municipios, index=municipios.index("CAMPINAS") if "CAMPINAS" in municipios else 0)
    df = df[df["Município"] == municipio_sel]

    st.markdown(f"**Total de registros:** {len(df)}")

    # Gráfico interativo: evolução anual dos gastos
    graf = df.groupby("Ano")["Liquidado"].sum().reset_index()

    fig = px.bar(
        graf,
        x="Ano",
        y="Liquidado",
        text_auto=".2s",
        labels={"Liquidado": "Valor Liquidado (R$)"},
        title=f"Dispêndios Públicos em C&T – {municipio_sel} (2016–2021)",
    )
    fig.update_layout(yaxis_tickprefix="R$ ", xaxis_title="Ano", yaxis_title="Total Liquidado")
    st.plotly_chart(fig, use_container_width=True)

    # Detalhamento por Programa
    graf2 = df.groupby(["Ano", "Programa"])["Liquidado"].sum().reset_index()

    fig2 = px.bar(
        graf2,
        x="Ano",
        y="Liquidado",
        color="Programa",
        labels={"Liquidado": "Valor Liquidado (R$)"},
        title=f"Programas de C&T em {municipio_sel}",
    )
    fig2.update_layout(yaxis_tickprefix="R$ ", xaxis_title="Ano", yaxis_title="Total por Programa")
    st.plotly_chart(fig2, use_container_width=True)

    # Tabela com os dados filtrados
    with st.expander("Ver dados brutos filtrados"):
        st.dataframe(df.reset_index(drop=True), use_container_width=True)
