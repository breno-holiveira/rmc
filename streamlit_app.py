import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <style>
    /* Remove margem/padding superior do título principal */
    .css-1d391kg h1 {
        margin-top: 0.25rem;
    }
    /* Remove margem/padding superior do subtítulo */
    .css-1d391kg h3 {
        margin-top: 0.1rem;
        margin-bottom: 0.5rem;
    }
    /* Texto introdutório */
    .intro-text {
        font-size: 16px;
        max-width: 900px;
        color: #34495e;
        line-height: 1.5;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Texto de introdução explicativo
st.markdown(
    """
    <div class="intro-text">
    Bem-vindo ao painel interativo de dados da Região Metropolitana de Campinas (RMC). Aqui você pode explorar indicadores econômicos e demográficos atualizados dos municípios que compõem a região. 

    Utilize o mapa abaixo para selecionar um município e visualizar seus dados detalhados, como PIB, participação regional, população, área e densidade demográfica.

    Este painel é uma ferramenta dinâmica para apoiar análises, estudos e tomada de decisão com base em informações oficiais e atualizadas. Explore, compare e descubra as características da RMC de forma intuitiva e visual.
    </div>
    """,
    unsafe_allow_html=True,
)

# Carregamento de dados
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

# Construir GeoJSON (chaves normais aqui)
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

gj = {"type": "FeatureCollection", "features": features}
geojson_js = json.dumps(gj)

# Carregamento de HTML externo refinado
with open("grafico_rmc.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# Inserção do GeoJSON no HTML
html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

# Exibir no Streamlit
st.components.v1.html(html_code, height=600, scrolling=False)
