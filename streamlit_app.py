import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Importa a fonte Inter via Google Fonts
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">

<style>
/* Ajusta o container da navbar */
.stHorizontalBlock {
    background-color: #1f2937 !important;
    padding: 0 !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: left !important;
}

/* Estiliza os itens: span dentro da navbar */
.stHorizontalBlock span {
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    font-size: 13px !important;
    color: rgba(255,255,255,0.85) !important;
    padding: 6px 6px !important; /* padding horizontal reduzido */
    margin: 0 2px !important;   /* margem lateral reduzida para compactar espaçamento */
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
    transition: color 0.2s ease;
}

/* Hover nos itens */
.stHorizontalBlock span:hover {
    color: #ffa366 !important;
}

/* Item ativo - borda inferior simples e texto destacado */
.stHorizontalBlock [aria-selected="true"] span {
    font-weight: 500 !important;
    color: #ffffff !important;
    border-bottom: 2px solid rgba(255, 255, 255, 0.4) !important;
    padding-bottom: 4px !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border-radius: 0 !important;
}
</style>
""", unsafe_allow_html=True)

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "6px 6px",
        "font-weight": "400",
        "font-size": "13px",
        "margin": "0 2px",
    },
    "active": {
        "color": "#ffffff",
        "font-weight": "500",
        "border-bottom": "2px solid rgba(255, 255, 255, 0.4)",
        "padding-bottom": "4px",
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
