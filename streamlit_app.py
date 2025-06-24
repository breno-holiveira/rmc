import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from pathlib import Path

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# --- Leitura dos dados geográficos e da planilha
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel("dados_rmc.xlsx")
df.set_index("nome", inplace=True)

# --- Construção do GeoJSON com os dados combinados
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({
        "type": "Feature",
        "geometry": geom,
        "properties": props
    })

geojson = {
    "type": "FeatureCollection",
    "features": features
}
geojson_str = json.dumps(geojson, ensure_ascii=False)

# --- Leitura do HTML modelo externo
html_path = Path("map_template.html")
html_code = html_path.read_text(encoding="utf-8")

# --- Substituição do marcador de posição pelo GeoJSON
html_final = html_code.replace("__GEOJSON__", geojson_str)

# --- Exibição no Streamlit
st.components.v1.html(html_final, height=750, scrolling=False)
