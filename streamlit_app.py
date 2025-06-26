import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMCd Data", layout="wide", page_icon='📊', initial_sidebar_state="expanded")

from streamlit_navigation_bar import st_navbar

# Barra de navegação com retorno da aba selecionada
page = st_navbar(["Home", "Documentação", "Exemplos", "Sobre"])
st.markdown(f"<style>.stApp {{ padding-top: 1rem; }}</style>", unsafe_allow_html=True)

if page == "Home":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

    st.markdown("""
        A Região Metropolitana de Campinas foi criada em 2000, através da Lei Complementar nº 870 do estado de São Paulo 
        e é constituída por 20 municípios. Em 2021, a RMC apresentou um PIB de **266,8 bilhões de reais**, 
        o equivalente a **3,07%** do Produto Interno Bruto brasileiro no mesmo ano.
    """)

    st.markdown("""
        Em 2020, o Instituto Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de 
        [Campinas](https://www.ibge.gov.br/cidades-e-estados/sp/campinas.html) como uma das 15 metrópoles brasileiras.
    """)

    # Carregamento de dados
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    gdf = gdf.sort_values(by='NM_MUN')

    df = pd.read_excel('dados_rmc.xlsx')
    df.set_index("nome", inplace=True)

    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})

    gj = {"type": "FeatureCollection", "features": features}
    geojson_js = json.dumps(gj)

    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

    st.components.v1.html(html_code, height=600, scrolling=False)

elif page == "Documentação":
    st.title("📚 Documentação")
    st.write("Em construção.")

elif page == "Exemplos":
    st.title("🔍 Exemplos")
    st.write("Exemplos de uso do mapa e visualizações.")

elif page == "Sobre":
    st.title("ℹ️ Sobre")
    st.markdown("Desenvolvido por Breno Oliveira, com dados do IBGE e análises da RMC.")
