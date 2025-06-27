import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Inicializa o estado da página no session_state para controlar a aba ativa
if "page" not in st.session_state:
    st.session_state.page = "RMC Data"

# Configurar layout da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

logo_path = os.path.join(os.getcwd(), "cubes.svg")

# Importar fonte Inter e CSS personalizado para navbar
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        .stHorizontalBlock span {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-weight: 400 !important;
            font-size: 14px !important;
            letter-spacing: 0em !important;
            padding: 6px 6px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.85) !important;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: relative;
            transition: color 0.25s ease;
        }
        .stHorizontalBlock span:hover {
            color: #ff9e3b !important;
        }
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 500 !important;
            color: rgba(255,255,255,0.85) !important;
        }
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: none !important;
        }
        .stHorizontalBlock {
            background-color: #1f2937 !important;
            padding: 0 !important;
            height: 44px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
            user-select: none;
        }
        /* Ajustes para largura máxima da página */
        .css-18e3th9 { max-width: 100% !important; padding-left: 1rem !important; padding-right: 1rem !important; }
        .css-1d391kg { padding-left: 0 !important; padding-right: 0 !important; margin-left: 0 !important; margin-right: 0 !important; max-width: 100% !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
        "font-family": "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-size": "14px",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "6px 6px",
        "font-weight": "400",
        "font-size": "14px",
        "letter-spacing": "0em",
        "margin": "0 6px",
        "white-space": "nowrap",
        "position": "relative",
    },
    "active": {
        "color": "rgba(255,255,255,0.85)",
        "font-weight": "500",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
    "logo_href": "#",  # link para logo (clicar não muda de página, faremos manual)
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

# Função para capturar clique no logo: forçar página "RMC Data"
clicked_logo = st.experimental_get_query_params().get("logo_clicked", ["0"])[0]
if clicked_logo == "1":
    st.session_state.page = "RMC Data"
    st.experimental_set_query_params()  # limpa query params pra evitar loop

# Exibe a navbar, passando a página atual como "default"
page = st_navbar(
    pages,
    logo_path=logo_path,
    styles=styles,
    options=options,
    default=st.session_state.page,
)

# Atualiza a página selecionada no session_state
if page != st.session_state.page:
    st.session_state.page = page

# Conteúdo das páginas
if st.session_state.page == "RMC Data":
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

elif st.session_state.page == "Economia":
    st.title("Economia")
    st.write("Conteúdo relacionado à economia da Região Metropolitana de Campinas.")

elif st.session_state.page == "Finanças Públicas":
    st.title("Finanças Públicas")
    st.write("Informações sobre finanças públicas da região.")

elif st.session_state.page == "Segurança":
    st.title("Segurança")
    st.write("Dados e análises sobre segurança.")

elif st.session_state.page == "Arquivos":
    st.title("Arquivos")
    st.write("Documentos e arquivos relacionados ao projeto.")

elif st.session_state.page == "Sobre":
    st.title("Sobre")
    st.write("Informações institucionais e gerais sobre o projeto.")

elif st.session_state.page == "Contato":
    st.title("Contato")
    st.write("Informações para contato e comunicação.")
