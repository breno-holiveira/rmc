import streamlit as st
import geopandas as gpd
import json
from pathlib import Path

st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="collapsed")
st.title("RMC Data")
st.header("Dados e indicadores da Região Metropolitana de Campinas")

# Caminho do shapefile - ajuste conforme seu caminho local!
shapefile_path = "./shapefile_rmc/RMC_municipios.shp"

# Testa se o arquivo existe
if not Path(shapefile_path).exists():
    st.error(f"Shapefile não encontrado no caminho: {shapefile_path}")
    st.stop()

# Lê o shapefile
try:
    gdf = gpd.read_file(shapefile_path)
    st.success(f"Shapefile carregado com sucesso: {len(gdf)} municípios")
except Exception as e:
    st.error(f"Erro ao carregar shapefile: {e}")
    st.stop()

# Confere CRS e transforma se necessário
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
    st.info("Transformado CRS para EPSG:4326")

# Dados extras (população, área, PIB)
dados_extra = {
    "Americana": {"populacao": 240000, "area": 140.5, "pib_2021": 12500000000},
    "Artur Nogueira": {"populacao": 56000, "area": 140.2, "pib_2021": 2200000000},
    "Campinas": {"populacao": 1200000, "area": 796.0, "pib_2021": 105000000000},
    # ... (adicione todos os demais conforme antes)
}

# Criar GeoJSON
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    extra = dados_extra.get(nome, {"populacao": None, "area": None, "pib_2021": None})
    features.append({
        "type": "Feature",
        "properties": {
            "name": nome,
            "populacao": extra["populacao"],
            "area": extra["area"],
            "pib_2021": extra["pib_2021"]
        },
        "geometry": geom
    })

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

st.write("GeoJSON sample (primeira feature):")
st.json(features[0])

# Carregar HTML
html_path = Path("grafico.html")
if not html_path.exists():
    st.error(f"Arquivo HTML não encontrado: {html_path}")
    st.stop()

html = html_path.read_text(encoding="utf-8")

# Injeta GeoJSON no placeholder do HTML
html_injetado = html.replace(
    '<script id="geojson-data" type="application/json"></script>',
    f'<script id="geojson-data" type="application/json">{geojson_str}</script>'
)

# Exibe mapa no Streamlit
st.components.v1.html(html_injetado, height=650, scrolling=True)
