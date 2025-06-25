
# streamlit_app.py (trecho principal resumido)
# O HTML será atualizado com filtro integrado visualmente, e as cores agora usam escala por quantis

import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np

st.set_page_config(page_title="RMC Data", layout="wide")
st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregar dados
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
gdf = gdf.sort_values(by="NM_MUN")
df = pd.read_excel("dados_rmc.xlsx").set_index("nome")

# Nome da variável que virá do HTML (via js-to-python pode ser incorporado depois com streamlit_js_eval)
# Por enquanto, simulamos a escolha
coluna_destaque = "per_capita_2021"  # Exemplo fixo (vai virar variável interativa via JS)

# Normalização usando quantis
valores = df[coluna_destaque].dropna()
quantis = pd.qcut(valores, q=5, labels=False, duplicates="drop")
cmap = cm.get_cmap("viridis")

cores = {}
for nome in df.index:
    if nome in quantis.index:
        idx = quantis[nome]
        cor = mcolors.to_hex(cmap(idx / quantis.max()))
        cores[nome] = cor

# GeoJSON com cor por município
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    props["color"] = cores.get(nome, "#b6cce5")
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

# HTML (resumido para exportação)
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><style>
  /* Filtro visual integrado */
  #filter {{
    margin-bottom: 14px;
    font-size: 14px;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    width: 100%;
  }}
</style></head>
<body>
  <div id="sidebar">
    <h2>Municípios</h2>
    <select id="filter">
      <option value="pib_2021">PIB 2021</option>
      <option value="per_capita_2021" selected>PIB per capita</option>
      <option value="populacao_2022">População</option>
      <option value="densidade_demografica_2022">Densidade demográfica</option>
      <option value="participacao_rmc">% no PIB regional</option>
    </select>
    <input id="search" type="search" placeholder="Buscar município..." />
    <div id="list"></div>
  </div>
  <script>
    // Em breve: capturar mudança de filtro e enviar ao Python com streamlit_js_eval
    document.getElementById("filter").addEventListener("change", (e) => {{
        const variavel = e.target.value;
        alert("Você escolheu: " + variavel);  // trocar por callback real
    }});
  </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=700, scrolling=False)
