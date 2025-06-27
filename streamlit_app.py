import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# =================== INÍCIO: FONTE E BARRA SUPERIOR ===================
st.set_page_config(initial_sidebar_state="collapsed")

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
        .rmc-logo {
            font-family: 'DM Sans', sans-serif;
            font-weight: 600;
            font-size: 15px;
            color: white;
            text-decoration: none;
            padding: 12px 18px;
            display: inline-block;
        }
        .rmc-logo:hover {
            color: #ff9e3b;
        }
        .stHorizontalBlock span {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 400 !important;
            font-size: 14.5px !important;
            color: rgba(255,255,255,0.85) !important;
            margin: 0 6px !important;
            white-space: nowrap;
            position: relative;
        }
        .stHorizontalBlock span:hover {
            color: #ff9e3b !important;
        }
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 500 !important;
            color: rgba(255,255,255,0.95) !important;
        }
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: '';
            position: absolute;
            left: 10%;
            bottom: 0;
            height: 3px;
            width: 80%;
            background-color: #ff9e3b;
            border-radius: 4px;
            animation: underlineExpand 0.3s forwards;
        }
        .stHorizontalBlock {
            background-color: #1f2937 !important;
            height: 44px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
        }
        @keyframes underlineExpand {
            from { width: 0; }
            to { width: 80%; }
        }
    </style>

    <a href="/?page=RMC%20Data" class="rmc-logo">RMC DATA</a>
    """,
    unsafe_allow_html=True,
)

# =================== NAVEGAÇÃO ===================

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
        "font-family": "'DM Sans', sans-serif",
        "font-size": "14.5px",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "font-weight": "400",
        "font-size": "14.5px",
    },
    "active": {
        "color": "rgba(255,255,255,0.95)",
        "font-weight": "500",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = [
    "RMC Data",
    "Economia",
    "Finanças Públicas",
    "Segurança",
    "Arquivos",
    "Sobre",
    "Contato",
]

query_params = st.query_params
default_page = query_params.get("page", "RMC Data")

page = st_navbar(pages, styles=styles, options=options, default=default_page)

# =================== CONTEÚDO DAS PÁGINAS ===================

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
