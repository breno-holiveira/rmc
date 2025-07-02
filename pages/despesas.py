import streamlit as st
import pandas as pd
import plotly.express as px
import locale

# Define localidade brasileira para formatação
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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

def format_brl(x):
    return f"R$ {locale.format_string('%.2f', x, grouping=True)}"

def top_n_outros(df, grupo, valor, n=7):
    df_agg = df.groupby(grupo)[valor].sum().sort_values(ascending=False)
    top_n = df_agg.head(n)
    outros = df_agg[n:].sum()
    if outros > 0:
        top_n["Outros"] = outros
    return top_n.reset_index()

def show():
    st.title("Análise de Despesas em C&T (2016–2021)")

    df = load_data()

    # --- Critérios de inclusão (OU) ---
    subfun_ct = ["571", "572", "573", "606", "664", "665"]
    keywords = [
        "pesquisa", "científica", "cientifica", "ciencia", "inovacao", "desenvolvimento",
        "P&D", "tecnologia", "laboratório", "laboratorio", "inovação", "técnico", "tecnico", "ciência",
        "tecnológico", "tecnologico", "formação", "formacao", "universidade", "ensino", "acadêmica"
    ]

    mask_func = df["Função"].astype(str).str.strip() == "19"
    mask_subfunc = df["Subfunção"].astype(str).isin(subfun_ct)

    def keyword_mask(col):
        return col.astype(str).str.lower().str.contains('|'.join(keywords), na=False)

    mask_keywords = (
        keyword_mask(df["Programa"]) |
        keyword_mask(df["Ação"]) |
        keyword_mask(df["Despesa"])
    )

    df = df[mask_func | mask_subfunc | mask_keywords]

    excluir = ["inativos", "pensionistas", "juros", "amortização", "assistencia hospitalar"]
    mask_excluir = df["Despesa"].astype(str).str.lower().str.contains('|'.join(excluir), na=False)
    df = df[~mask_excluir]

    # --- Filtro por município ---
    municipios = sorted(df["Município"].dropna().unique())
    municipio_sel = st.selectbox(
        "Selecione o município",
        municipios,
        index=municipios.index("CAMPINAS") if "CAMPINAS" in municipios else 0
    )
    df = df[df["Município"] == municipio_sel]

    st.markdown(f"**Total de registros encontrados:** `{len(df)}`")

    # --- Gráfico 1: Total por ano ---
    dados_ano = df.groupby("Ano")["Liquidado"].sum().reset_index()
    fig1 = px.bar(
        dados_ano, x="Ano", y="Liquidado", text_auto=".2s",
        title=f"Total de Despesas em C&T – {municipio_sel}",
        labels={"Liquidado": "Valor Liquidado (R$)"},
    )
    fig1.update_layout(
        yaxis_tickprefix="R$ ",
        xaxis_title="Ano",
        yaxis_title="Total Liquidado",
        title_x=0.05
    )
    fig1.update_traces(texttemplate='%{text:.2s}', hovertemplate='Ano: %{x}<br>R$ %{y:,.2f}<extra></extra>')
    st.plotly_chart(fig1, use_container_width=True)

    # --- Gráfico 2: Por Programa ---
    top_programas = top_n_outros(df, "Programa", "Liquidado")
    fig2 = px.bar(
        top_programas, x="Programa", y="Liquidado",
        title=f"Top 7 Programas de C&T – {municipio_sel}",
        labels={"Liquidado": "Valor Liquidado (R$)"},
    )
    fig2.update_layout(xaxis_title="Programa", yaxis_tickprefix="R$ ", title_x=0.05)
    fig2.update_traces(hovertemplate='%{x}<br>R$ %{y:,.2f}<extra></extra>')
    st.plotly_chart(fig2, use_container_width=True)

    # --- Gráfico 3: Por Órgão ---
    top_orgaos = top_n_outros(df, "Órgão", "Liquidado")
    fig3 = px.bar(
        top_orgaos, x="Órgão", y="Liquidado",
        title=f"Top 7 Órgãos em C&T – {municipio_sel}",
        labels={"Liquidado": "Valor Liquidado (R$)"},
    )
    fig3.update_layout(xaxis_title="Órgão", yaxis_tickprefix="R$ ", title_x=0.05)
    fig3.update_traces(hovertemplate='%{x}<br>R$ %{y:,.2f}<extra></extra>')
    st.plotly_chart(fig3, use_container_width=True)

    # --- Gráfico 4: Por Unidade Orçamentária (UO) ---
    top_uo = top_n_outros(df, "UO", "Liquidado")
    fig4 = px.bar(
        top_uo, x="UO", y="Liquidado",
        title=f"Top 7 UOs em C&T – {municipio_sel}",
        labels={"Liquidado": "Valor Liquidado (R$)"},
    )
    fig4.update_layout(xaxis_title="Unidade Orçamentária", yaxis_tickprefix="R$ ", title_x=0.05)
    fig4.update_traces(hovertemplate='%{x}<br>R$ %{y:,.2f}<extra></extra>')
    st.plotly_chart(fig4, use_container_width=True)

    # --- Gráfico 5: Por Unidade Gestora ---
    top_gestora = top_n_outros(df, "Unidade Gestora", "Liquidado")
    fig5 = px.bar(
        top_gestora, x="Unidade Gestora", y="Liquidado",
        title=f"Top 7 Unidades Gestoras – {municipio_sel}",
        labels={"Liquidado": "Valor Liquidado (R$)"},
    )
    fig5.update_layout(xaxis_title="Unidade Gestora", yaxis_tickprefix="R$ ", title_x=0.05)
    fig5.update_traces(hovertemplate='%{x}<br>R$ %{y:,.2f}<extra></extra>')
    st.plotly_chart(fig5, use_container_width=True)

    # --- Tabela final com valor formatado ---
    df["Liquidado (R$)"] = df["Liquidado"].apply(format_brl)
    with st.expander("Ver dados brutos filtrados"):
        st.dataframe(df[["Ano", "Município", "Programa", "Órgão", "UO", "Unidade Gestora", "Liquidado (R$)"]], use_container_width=True)
