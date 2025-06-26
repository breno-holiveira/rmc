import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# Estilos da barra (substitui o CSS anterior)
styles = {
    "nav": {
        "background-color": "linear-gradient(90deg, #0d1f3c, #163466)",
        "justify-content": "center",
        "border-radius": "0 0 15px 15px",
        "box-shadow": "0 3px 8px rgb(0 0 0 / 0.3)",
        "padding": "0.6rem 1rem",
    },
    "span": {
        "color": "white",
        "padding": "10px 14px",
        "font-family": "Roboto, sans-serif",
        "font-size": "1.05rem",
        "font-weight": "600",
    },
    "active": {
        "background-color": "#ff7200",
        "color": "white",
        "font-weight": "700",
        "box-shadow": "0 0 8px 1px #ff7f27",
        "border-radius": "8px",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = ["Home", "Documentation", "Examples", "Community", "About"]
page = st_navbar(pages, styles=styles, options=options)

# Conteúdo das páginas
if page == "Home":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

    st.markdown(
        "A Região Metropolitana de Campinas foi criada em 2000, através da Lei Complementar nº 870, do estado de São Paulo e é constituída por 20 municípios. "
        "Em 2021, a RMC apresentou um PIB de 266,8 bilhões de reais, o equivalente a 3,07% do Produto Interno Bruto brasileiro no mesmo ano."
    )
    st.markdown(
        "Em 2020, o Instituto Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de Campinas como uma das 15 metrópoles brasileiras."
    )

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

    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

elif page == "Documentation":
    st.title("Documentation")
    st.write("Aqui você pode colocar a documentação do seu app...")

elif page == "Examples":
    st.title("Examples")
    st.write("Exemplos do app...")

elif page == "Community":
    st.title("Community")
    st.write("Links para a comunidade...")

elif page == "About":
    st.title("About")
    st.write("Sobre o projeto...")
