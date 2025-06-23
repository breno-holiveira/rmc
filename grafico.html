import streamlit as st
import geopandas as gpd
import json
from pathlib import Path

st.set_page_config(layout="wide")
st.title('RMC Data')
st.header('Dados e indicadores da Região Metropolitana de Campinas')

# → Aqui vem seu `dados_extra` conforme já está

gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
gdf = gdf.sort_values(by="NM_MUN")

geojson = {"type":"FeatureCollection","features":[]}
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    extra = dados_extra.get(nome, {})
    geojson["features"].append({
        "type":"Feature",
        "properties":{"name":nome, **extra},
        "geometry":geom
    })

geojson_str = json.dumps(geojson)

html = Path("grafico.html").read_text(encoding="utf-8")
html = html.replace("{{geojson}}", geojson_str)

st.components.v1.html(html, height=700, scrolling=True)
