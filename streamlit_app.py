import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Estado inicial
if "page" not in st.session_state:
    st.session_state.page = "RMC Data"

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊",
)

# Fonte DM Sans + CSS igual ao da OUP, mantendo azul escuro
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
        .stHorizontalBlock {
            background-color: #1f2937 !important;
            height: 56px !important;
            padding: 0 32px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .stHorizontalBlock span {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 400 !important;
            font-size: 16px !important;
            color: rgba(255, 255, 255, 0.88) !important;
            margin: 0 10px !important;
            padding: 6px 12px !important;
            border-radius: 6px;
            transition: background-color 0.2s ease, color 0.2s ease;
        }
        .stHorizontalBlock span:hover {
            background-color: rgba(255,255,255,0.08);
        }
        .stHorizontalBlock [aria-selected="true"] span {
            background-color: rgba(255,255,255,0.14);
            color: #f4a259 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Estilos do st_navbar (compatíveis com o CSS acima)
styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
        "font-family": "'DM Sans', sans-serif",
        "font-size": "16px",
    },
    "span": {
        "color": "rgba(255, 255, 255, 0.88)",
        "padding": "6px 12px",
        "margin": "0 10px",
        "font-weight": "400",
        "border-radius": "6px",
    },
    "active": {
        "color": "#f4a259",
        "background-color": "rgba(255,255,255,0.14)",
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

clicked_page = st_navbar(pages, logo_path=None, styles=styles, options=options)

if clicked_page and clicked_page != st.session_state.page:
    st.session_state.page = clicked_page

page = st.session_state.page

# Página: RMC Data
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

    # Carregamento de dados
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
