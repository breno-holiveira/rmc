import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Caminho para o logo cubes.svg na pasta raiz
logo_path = os.path.join(os.getcwd(), "cubes.svg")

# Importar fonte Inter para suavidade e legibilidade
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        /* Estilo base dos itens da navbar */
        .stHorizontalBlock span {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-weight: 400 !important;
            font-size: 15px !important;
            letter-spacing: 0em !important;
            padding: 6px 6px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.85) !important;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: relative;
            transition: color 0.15s ease, background-color 0.15s ease;
        }
        /* Hover suave: só muda a cor */
        .stHorizontalBlock span:hover {
            color: #ff9e3b !important;
        }
        /* Destaque do item ativo para todas as abas (menos RMC Data) */
        .stHorizontalBlock [aria-selected="true"] span:not(.rmc-data) {
            font-weight: 500 !important;
            color: rgba(255,255,255,0.95) !important;
            background-color: transparent !important;
        }
        /* Fundo branco sutil para RMC Data quando ativo */
        .stHorizontalBlock [aria-selected="true"] span.rmc-data {
            font-weight: 500 !important;
            color: rgba(255,255,255,0.95) !important;
            background-color: rgba(255,255,255,0.12) !important;
            border-radius: 6px;
            padding-left: 12px !important;
            padding-right: 12px !important;
        }
        /* Linha sublinhada discreta fixa embaixo do item ativo */
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: '';
            position: absolute;
            left: 10%;
            bottom: 0;
            height: 2px;
            width: 80%;
            background-color: #ff9e3b;
            border-radius: 3px;
        }
        /* Container da navbar */
        .stHorizontalBlock {
            background-color: #1f2937 !important; /* cinza escuro */
            padding: 0 !important;
            height: 44px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
            user-select: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
        "font-family": "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-size": "15px",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "6px 6px",
        "font-weight": "400",
        "font-size": "15px",
        "letter-spacing": "0em",
        "margin": "0 6px",
        "white-space": "nowrap",
        "position": "relative",
    },
    "active": {
        "color": "rgba(255,255,255,0.95)",
        "font-weight": "500",
        "background-color": "transparent",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = [
    "RMC Data",
    "Sobre",
    "Economia",
    "Finanças Públicas",
    "Segurança",
    "População",
]

page = st_navbar(
    pages,
    logo_path=logo_path,
    styles=styles,
    options=options,
    # Adiciona a classe rmc-data só ao span do primeiro item para CSS específico
    item_classnames=["rmc-data"] + [""] * (len(pages) - 1),
)

# Conteúdo por página

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

elif page == "Sobre":
    st.title("Sobre")
    st.write("Informações institucionais e gerais sobre o projeto.")

elif page == "Economia":
    st.title("Economia")
    st.write("Conteúdo relacionado à economia da RMC.")

elif page == "Finanças Públicas":
    st.title("Finanças Públicas")
    st.write("Informações sobre finanças públicas da região.")

elif page == "Segurança":
    st.title("Segurança")
    st.write("Dados e análises sobre segurança.")

elif page == "População":
    st.title("População")
    st.write("Indicadores populacionais da Região Metropolitana de Campinas.")
