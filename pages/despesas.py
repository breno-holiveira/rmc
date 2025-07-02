# pages/despesas.py

import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data(show_spinner=False)
def load_data(path="despesas_sp.xlsx"):
    # 1) Leitura e limpeza inicial
    df = (
        pd.read_excel(path, parse_dates=["Ano"])
          .rename(columns=lambda c: c.strip())
    )
    # Remove espaços nas strings
    for col in df.select_dtypes("object"):
        df[col] = df[col].str.strip()
    # Converte moeda para float
    for col in ["Despesa", "Liquidado"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[R$\.\s]", "", regex=True)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )
    return df

def show():
    st.markdown("## Análise de Despesas em C&T (2016–2021)")

    df = load_data()

    # --- 0) Filtra intervalo de anos
    anos = st.slider(
        "Período (Ano)", 
        min_value=int(df["Ano"].dt.year.min()),
        max_value=int(df["Ano"].dt.year.max()),
        value=(2016, 2021),
        step=1
    )
    df = df[df["Ano"].dt.year.between(anos[0], anos[1])]

    # --- 1) Função 19: Pesquisa e Desenvolvimento (Frascati)
    df1 = df[df["Função"].str.startswith("19")]

    # --- 2) Subfunções Frascati (códigos oficiais)
    SUB_FUNCS = {
        "571": "Desenvolvimento Científico",
        "572": "Desenvolvimento Tecnológico e Engenharia",
        "573": "Difusão do Conhecimento Científico e Tecnológico",
        "606": "Extensão Rural",
        "664": "Propriedade Industrial",
        "665": "Normalização e Qualidade",
    }
    df2 = df1[df1["Subfunção"].isin(SUB_FUNCS.keys())]

    # --- 3) RIECTI / Keywords adicionais
    kw = st.text_input(
        "Palavras‑chave livres (separe por vírgula)",
        value="INOVAÇÃO,CIÊNCIA,TECNOLOGIA,PESQUISA,DESENVOLVIMENTO"
    )
    termos = [t.strip().upper() for t in kw.split(",") if t.strip()]
    if termos:
        pattern = "|".join(termos)
        mask3 = (
            df2["Programa"].str.upper().str.contains(pattern) |
            df2["Ação"].str.upper().str.contains(pattern) |
            df2["Funcional Programática"].str.upper().str.contains(pattern)
        )
        df3 = df2[mask3]
    else:
        df3 = df2

    # --- 4) Consolida filtros e remove duplicatas
    df_ct = (
        pd.concat([df1, df2, df3])
          .drop_duplicates(subset=["Ano","Órgão","UO","Unidade Gestora",
                                   "Programa","Ação","Funcional Programática",
                                   "Credor","Despesa","Liquidado"])
          .sort_values("Ano")
    )

    # --- 5) Agregações para gráficos
    df_ano = (
        df_ct
        .groupby(df_ct["Ano"].dt.year.rename("Ano"))
        .agg(Total_Despesa=("Despesa","sum"),
             Total_Liquidado=("Liquidado","sum"))
        .reset_index()
    )

    df_sub = (
        df_ct
        .groupby("Subfunção")
        .agg(Despesa=("Despesa","sum"))
        .reset_index()
        .assign(Subfunção=lambda d: d["Subfunção"].map(SUB_FUNCS))
    )

    # --- Exibição de métricas
    st.markdown("### Resumo Geral")
    col1, col2 = st.columns(2)
    col1.metric("Total Despesa C&T (2016–2021)", f"R$ {df_ct['Despesa'].sum():,.2f}")
    col2.metric("Total Liquidado C&T",           f"R$ {df_ct['Liquidado'].sum():,.2f}")

    # --- Gráfico 1: Série Temporal (Despesa x Ano)
    st.markdown("### Evolução Anual da Despesa")
    line = (
        alt.Chart(df_ano)
           .mark_line(point=True)
           .encode(
               x="Ano:O",
               y=alt.Y("Total_Despesa:Q", title="Despesa (R$)"),
               tooltip=["Ano","Total_Despesa"]
           )
           .interactive()
    )
    st.altair_chart(line, use_container_width=True)

    # --- Gráfico 2: Participação por Subfunção
    st.markdown("### Despesa por Subfunção (C&T)")
    bar = (
        alt.Chart(df_sub)
           .mark_bar()
           .encode(
               y=alt.Y("Subfunção:N", sort="-x"),
               x=alt.X("Despesa:Q", title="Total Despesa (R$)"),
               tooltip=["Subfunção","Despesa"]
           )
           .interactive()
    )
    st.altair_chart(bar, use_container_width=True)

    # --- Tabela detalhada filtrada
    st.markdown("### Detalhamento das Despesas C&T")
    with st.expander("Mostrar base filtrada completa"):
        st.dataframe(df_ct.reset_index(drop=True), height=400)

    # --- Download CSV
    csv = df_ct.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Baixar dados C&T (CSV)", csv, "despesas_ct_2016_2021.csv", "text/csv"
    )
