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
        st.warning("Nenhum dado disponível após a limpeza.")
        return
    # obter anos disponíveis
    years = sorted(df['Ano'].dt.year.unique())
    # Se houver mais de um ano, ofereça slider, senão apenas selecione
    if len(years) > 1:
        try:
            default_min = max(2016, years[0])
            default_max = min(2021, years[-1])
            sel_years = st.slider(
                "Período (Ano)",
                min_value=years[0],
                max_value=years[-1],
                value=(default_min, default_max),
                step=1
            )
        except Exception:
            sel_years = (years[0], years[-1])
    else:
        sel_years = (years[0], years[0])
    # filtra
    df = df[df['Ano'].dt.year.between(sel_years[0], sel_years[1])]
    if df.empty:
        st.warning("Nenhum dado no período selecionado.")
        return
    # Filtragem Frascati
    df1 = df[df["Função"].str.startswith("19")]
    SUB_FUNCS = {"571":"Desenvolvimento Científico","572":"Desenvolvimento Tecnológico e Engenharia","573":"Difusão do Conhecimento Científico e Tecnológico","606":"Extensão Rural","664":"Propriedade Industrial","665":"Normalização e Qualidade"}
    df2 = df1[df1["Subfunção"].isin(SUB_FUNCS.keys())]
    # filtro keywords
    kw = st.text_input("Palavras‑chave (comma)", value="INOVAÇÃO,CIÊNCIA,TECNOLOGIA")
    terms = [t.strip().upper() for t in kw.split(",") if t.strip()]
    if terms:
        pat = "|".join(terms)
        df3 = df2[df2["Programa"].str.upper().str.contains(pat) | df2["Ação"].str.upper().str.contains(pat) | df2["Funcional Programática"].str.upper().str.contains(pat)]
    else:
        df3 = df2
    # consolida
    df_ct = pd.concat([df1, df2, df3]).drop_duplicates(subset=["Ano","Órgão","UO","Unidade Gestora","Programa","Ação","Funcional Programática","Credor","Despesa","Liquidado"]).sort_values("Ano")
    if df_ct.empty:
        st.warning("Sem resultados após filtros.")
        return
    # agregações
    df_ano = df_ct.groupby(df_ct['Ano'].dt.year.rename('Ano')).agg(Total_Despesa=('Despesa','sum')).reset_index()
    # exibe
    st.metric("Total Despesa C&T", f"R$ {df_ct['Despesa'].sum():,.2f}")
    chart = alt.Chart(df_ano).mark_line(point=True).encode(x='Ano:O', y=alt.Y('Total_Despesa:Q', title='Despesa (R$)'), tooltip=['Ano','Total_Despesa']).interactive()
    st.altair_chart(chart, use_container_width=True)
    with st.expander("Detalhes"):
        st.dataframe(df_ct)
