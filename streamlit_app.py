import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Injeta CSS poderoso para reduzir espaçamento na navbar do st_navbar
st.markdown("""
<style>
/* Container da navbar */
[data-testid="stHorizontalBlock"] > div:first-child {
    background-color: #1f2937 !important;
    padding: 0 !important;
    height: 38px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: left !important;
}

/* Itens da navbar: botões e tabs */
[data-testid="stHorizontalBlock"] button,
[data-testid="stHorizontalBlock"] div[role="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    font-size: 13px !important;
    color: rgba(255,255,255,0.85) !important;
    padding: 4px 6px !important;       /* padding menor */
    margin: 0 4px !important;          /* margem lateral reduzida */
    border-radius: 0 !important;       /* borda reta */
    background-color: transparent !important;
    border: none !important;
    transition: color 0.2s ease, background-color 0.2s ease;
    cursor: pointer;
    white-space: nowrap;
}

/* Hover suave */
[data-testid="stHorizontalBlock"] button:hover,
[data-testid="stHorizontalBlock"] div[role="tab"]:hover {
    color: #ffa366 !important;
    background-color: transparent !important;
}

/* Item ativo: borda inferior fina */
[data-testid="stHorizontalBlock"] button[aria-selected="true"],
[data-testid="stHorizontalBlock"] div[role="tab"][aria-selected="true"] {
    color: #ffffff !important;
    font-weight: 500 !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border-bottom: 2px solid rgba(255, 255, 255, 0.4) !important;
    padding-bottom: 4px !important;
    margin-bottom: 0 !important;
}

/* Remove outline ao focar */
[data-testid="stHorizontalBlock"] button:focus,
[data-testid="stHorizontalBlock"] div[role="tab"]:focus {
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
        # fonte e tamanho já ajustados via CSS injetado
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "4px 6px",
        "font-weight": "400",
        "font-size": "13px",
        "margin": "0 4px",
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
