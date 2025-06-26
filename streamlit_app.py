import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="RMC Data", layout="wide", page_icon='📊')

# ESTILIZAÇÃO PERSONALIZADA DA NAVBAR
st.markdown("""
    <style>
    /* Container da barra */
    .st-navbar {
        background-color: #f8f9fa !important;
        border-bottom: 1px solid #ddd;
        padding: 10px 30px;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Itens da barra */
    .st-navbar span {
        margin-right: 25px;
        font-size: 16px;
        font-weight: 500;
        color: #34495e !important;
        text-decoration: none !important;
    }

    /* Aba ativa */
    .st-navbar span.active {
        color: #2c3e70 !important;
        border-bottom: 2px solid #2c3e70;
        padding-bottom: 4px;
    }

    /* Remove efeitos exagerados de hover */
    .st-navbar span:hover {
        color: #2c3e70 !important;
        background-color: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# BARRA DE NAVEGAÇÃO
page = st_navbar(["Início", "Documentação", "Exemplos", "Sobre"])
st.write("")  # Espaço opcional após a barra

# TÍTULO E INTRODUÇÃO
st.title("RMC Data 📊")
st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

st.markdown("""
A Região Metropolitana de Campinas foi criada em 2000 por meio da Lei Complementar nº 870. 
Atualmente, é composta por 20 municípios e representa **3,07%** do PIB brasileiro.

Em 2021, a RMC teve um PIB de **R$ 266,8 bilhões**, e em 2020, o IBGE classificou Campinas como uma das 15 metrópoles brasileiras.
""")

# CARREGAMENTO DE DADOS
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

# CRIAÇÃO DO GEOJSON PARA O MAPA
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson_js = json.dumps({"type": "FeatureCollection", "features": features})

# INSERÇÃO DO GEOJSON NO HTML EXTERNO
with open("grafico_rmc.html", "r", encoding="utf-8") as f:
    html_template = f.read()

html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

# EXIBIÇÃO DO MAPA
st.components.v1.html(html_code, height=620, scrolling=False)
