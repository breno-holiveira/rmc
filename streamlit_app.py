import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# ESTILO PERSONALIZADO PARA A BARRA
st.markdown("""
    <style>
    .st-navbar {
        background: linear-gradient(to right, #ffffff, #f2f4f7);
        border-bottom: 1px solid #ddd;
        padding: 12px 40px;
        font-family: 'Segoe UI', sans-serif;
        display: flex;
        gap: 30px;
        font-size: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .st-navbar span {
        color: #444;
        padding-bottom: 4px;
        transition: all 0.3s ease;
        cursor: pointer;
        border-bottom: 2px solid transparent;
    }

    .st-navbar span:hover {
        color: #2c3e70;
        border-bottom: 2px solid #a6b2c3;
    }

    .st-navbar span.active {
        color: #2c3e70;
        border-bottom: 2px solid #2c3e70;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# BARRA DE NAVEGAÇÃO
page = st_navbar(["Início", "Indicadores", "Mapa", "Sobre"])
st.write("")  # Pequeno espaçamento abaixo da barra

# TÍTULO E TEXTO INICIAL
st.title("RMC Data 📊")
st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

st.markdown("""
A Região Metropolitana de Campinas (RMC), formada por 20 municípios, representa **3,07%** do PIB nacional.  
Criada pela Lei Complementar nº 870 de 2000, a RMC é uma das regiões mais dinâmicas do Brasil.

Em 2021, o PIB da RMC foi de **R$ 266,8 bilhões**, enquanto o PIB brasileiro totalizou **R$ 8,7 trilhões**.
""")

# CARREGAMENTO DOS DADOS
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel("dados_rmc.xlsx")
df.set_index("nome", inplace=True)

# CRIAÇÃO DO GEOJSON
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

gj = {"type": "FeatureCollection", "features": features}
geojson_js = json.dumps(gj)

# INSERÇÃO DO GEOJSON NO HTML
with open("grafico_rmc.html", "r", encoding="utf-8") as f:
    html_template = f.read()

html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

# EXIBIÇÃO DO MAPA INTERATIVO
st.components.v1.html(html_code, height=620, scrolling=False)
