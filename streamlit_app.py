import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="expanded")

# CSS para formatação da apresentação inicial
st.markdown(
    """
    <style>
    /* Fonte principal e alinhamento */
    .main-container {
        max-width: 900px;
        margin: auto;
        padding: 2rem 1rem 3rem 1rem;
        color: #34495e;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
    }

    /* Título principal */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #2c3e70;
        margin-bottom: 0.2rem;
        line-height: 1.1;
    }

    /* Subtítulo */
    .subtitle {
        font-size: 1.5rem;
        font-weight: 500;
        color: #4d648d;
        margin-top: 0;
        margin-bottom: 1.5rem;
        font-style: italic;
    }

    /* Parágrafo texto */
    .intro-text {
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Linha horizontal sutil */
    .divider {
        border: none;
        border-top: 1px solid #d1d9e6;
        margin-bottom: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Conteúdo da apresentação inicial
st.markdown(
    """
    <div class="main-container">
      <h1 class="main-title">RMC Data</h1>
      <h2 class="subtitle">Indicadores econômicos e demográficos da Região Metropolitana de Campinas</h2>
      <p class="intro-text">
        Este painel interativo permite explorar de forma intuitiva e visual os dados econômicos e sociais dos municípios que compõem a Região Metropolitana de Campinas. 
        Navegue pelo mapa, selecione municípios e consulte informações atualizadas como PIB, população, área territorial e outros indicadores relevantes.
      </p>
      <hr class="divider" />
    </div>
    """,
    unsafe_allow_html=True,
)

# Carregamento dos dados geográficos e econômicos
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

# Construção do GeoJSON para o gráfico/mapa
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

gj = {"type": "FeatureCollection", "features": features}
geojson_js = json.dumps(gj)

# Leitura do HTML do mapa
with open("grafico_rmc.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# Inserção do GeoJSON no HTML
html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

# Exibição do mapa interativo na página
st.components.v1.html(html_code, height=600, scrolling=False)
