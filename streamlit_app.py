import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

styles = {
    "nav": {
        "background": "linear-gradient(90deg, #1e2a38, #273544)",
        "justify-content": "left",
        "font-family": "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-size": "14px",
        "padding": "0 10px",
        "height": "38px",
        "align-items": "center",
        "box-shadow": "none",
        "border-radius": "0",  # Remove bordas arredondadas da navbar
        "letter-spacing": "0.03em",
    },
    "span": {
        "color": "rgba(255, 255, 255, 0.85)",
        "padding": "6px 18px",  # Espaçamento lateral simétrico e maior para todas as opções
        "font-weight": "400",
        "user-select": "none",
        "transition": "color 0.25s ease",
        "margin": "0 6px",  # Margem para garantir espaçamento uniforme
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.18)",  # Fundo suave e translúcido
        "color": "#e6e6e6",  # Texto claro, mas não branco puro
        "font-weight": "600",
        "padding": "6px 18px",
        "border-radius": "2px",  # Bordas levemente arredondadas só para suavizar
        "user-select": "none",
        "box-shadow": "none",  # Remove sombra para menos destaque pesado
        "transition": "background-color 0.3s ease, color 0.3s ease",
        "margin": "0 6px",  # Mesma margem para alinhamento
    },
    "img": {
        "display": "none",  # Ocultar logo, só texto
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = ["Inicio", "Documentation", "Examples", "Community", "About"]

page = st_navbar(pages, styles=styles, options=options)

if page == "Inicio":
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
