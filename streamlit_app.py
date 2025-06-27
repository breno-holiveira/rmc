import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Estado inicial da página
if "page" not in st.session_state:
    st.session_state.page = "RMC Data"

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊",
)

# Estilo baseado no exemplo fornecido, adaptado para azul-escuro (#1f2937)
styles = {
    "nav": {
        "background-color": "#1f2937",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgba(255, 255, 255, 0.9)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
        "font-family": "'DM Sans', sans-serif",
        "font-size": "15px",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.2)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.1)",
    },
}

# Opções visuais
options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Páginas da barra
pages = [
    "RMC Data",
    "Economia",
    "Finanças Públicas",
    "Segurança",
    "Arquivos",
    "Sobre",
    "Contato",
]

# Barra de navegação
clicked_page = st_navbar(pages, styles=styles, options=options)
if clicked_page and clicked_page != st.session_state.page:
    st.session_state.page = clicked_page

page = st.session_state.page

# Conteúdo da página selecionada
if page == "RMC Data":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")
    st.markdown(
        "A Região Metropolitana de Campinas foi criada em 2000, através da Lei Complementar nº 870, do estado de São Paulo e é constituída por 20 municípios. "
        "Em 2021, a RMC apresentou um PIB de 266,8 bilhões de reais, o equivalente a 3,07% do Produto Interno Bruto brasileiro no mesmo ano."
    )
    st.markdown(
        "Em 2020, o Instituto Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de Campinas como uma das 15 metrópoles brasileiras."
    )

    # Dados do mapa
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values(by="NM_MUN")

    df = pd.read_excel("dados_rmc.xlsx")
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

    html_code = html_template.replace(
        "const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};"
    )
    st.components.v1.html(html_code, height=600, scrolling=False)

elif page == "Economia":
    st.title("Economia")
    st.write("Conteúdo relacionado à economia da Região Metropolitana de Campinas.")

elif page == "Finanças Públicas":
    st.title("Finanças Públicas")
    st.write("Informações sobre finanças públicas da região.")

elif page == "Segurança":
    st.title("Segurança")
    st.write("Dados e análises sobre segurança.")

elif page == "Arquivos":
    st.title("Arquivos")
    st.write("Documentos e arquivos relacionados ao projeto.")

elif page == "Sobre":
    st.title("Sobre")
    st.write("Informações institucionais e gerais sobre o projeto.")

elif page == "Contato":
    st.title("Contato")
    st.write("Informações para contato e comunicação.")
