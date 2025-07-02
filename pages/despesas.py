import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data(show_spinner=False)
def load_data(path="despesas_sp.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    df['Ano'] = pd.to_datetime(df['Ano'], errors='coerce')
    for col in df.select_dtypes("object"):
        df[col] = df[col].str.strip()

    def clean_money(col_series):
        s = (
            col_series.astype(str)
                      .str.replace(r"[R$\s]", "", regex=True)
                      .str.replace(r"\.", "", regex=True)
                      .str.replace(",", ".", regex=False)
        )
        return pd.to_numeric(s, errors="coerce")

    df["Despesa"]   = clean_money(df["Despesa"])
    df["Liquidado"] = clean_money(df["Liquidado"])
    df = df.dropna(subset=["Despesa", "Ano"])
    return df


def show():
    st.markdown("## Análise de Despesas em C&T (2016–2021)")
    df = load_data()

    if df.empty:
        st.warning("Nenhum dado disponível após a limpeza. Confira o arquivo ou critérios de limpeza.")
        return

    anos_vals = df["Ano"].dt.year
    min_ano, max_ano = int(anos_vals.min()), int(anos_vals.max())
    if min_ano > max_ano:
        st.warning("Intervalo de anos inválido.")
        return

    anos = st.slider(
        "Período (Ano)",
        min_value=min_ano,
        max_value=max_ano,
        value=(2016 if 2016>=min_ano else min_ano, 2021 if 2021<=max_ano else max_ano),
        step=1
    )
    df = df[anos_vals.between(anos[0], anos[1])]

    df1 = df[df["Função"].str.startswith("19")]
    SUB_FUNCS = {"571":"Desenvolvimento Científico","572":"Desenvolvimento Tecnológico e Engenharia","573":"Difusão do Conhecimento Científico e Tecnológico","606":"Extensão Rural","664":"Propriedade Industrial","665":"Normalização e Qualidade"}
    df2 = df1[df1["Subfunção"].isin(SUB_FUNCS.keys())]

    kw = st.text_input("Palavras‑chave livres (Programa, Ação ou Funcional Programática)","INOVAÇÃO,CIÊNCIA,TECNOLOGIA,PESQUISA,DESENVOLVIMENTO")
    termos = [t.strip().upper() for t in kw.split(",") if t.strip()]
    if termos:
        pattern = "|".join(termos)
        mask3 = df2["Programa"].str.upper().str.contains(pattern) | df2["Ação"].str.upper().str.contains(pattern) | df2["Funcional Programática"].str.upper().str.contains(pattern)
        df3 = df2[mask3]
    else:
        df3 = df2

    df_ct = pd.concat([df1, df2, df3]).drop_duplicates(subset=["Ano","Órgão","UO","Unidade Gestora","Programa","Ação","Funcional Programática","Credor","Despesa","Liquidado"]).sort_values("Ano")
    if df_ct.empty:
        st.warning("Nenhum registro encontrado para os critérios selecionados.")
        return

    df_ano = df_ct.groupby(df_ct["Ano"].dt.year.rename("Ano")).agg(Total_Despesa=("Despesa","sum"),Total_Liquidado=("Liquidado","sum")).reset_index()
    df_sub = df_ct.groupby("Subfunção").agg(Despesa=("Despesa","sum")).reset_index().assign(Subfunção=lambda d: d["Subfunção"].map(SUB_FUNCS))

    st.markdown("### Resumo Geral")
    col1,col2 = st.columns(2)
    col1.metric("Total Despesa C&T",f"R$ {df_ct['Despesa'].sum():,.2f}")
    col2.metric("Total Liquidado C&T",f"R$ {df_ct['Liquidado'].sum():,.2f}")

    st.markdown("### Evolução Anual da Despesa")
    chart1 = alt.Chart(df_ano).mark_line(point=True).encode(x="Ano:O",y=alt.Y("Total_Despesa:Q",title="Despesa (R$)"),tooltip=["Ano","Total_Despesa"]).interactive()
    st.altair_chart(chart1,use_container_width=True)

    st.markdown("### Despesa por Subfunção (C&T)")
    chart2 = alt.Chart(df_sub).mark_bar().encode(y=alt.Y("Subfunção:N",sort="-x"),x=alt.X("Despesa:Q",title="Total Despesa (R$)"),tooltip=["Subfunção","Despesa"]).interactive()
    st.altair_chart(chart2,use_container_width=True)

    st.markdown("### Detalhamento")
    with st.expander("Mostrar base filtrada completa"):
        st.dataframe(df_ct.reset_index(drop=True),height=400)

    csv = df_ct.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar CSV",data=csv,file_name="despesas_ct.csv",mime="text/csv")
