import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")
st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregamento dos dados
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

# Variável que será destacada (fixa por enquanto, em breve dinâmica)
coluna_destaque = "per_capita_2021"

# Normalização por quantis e coloração com cmap
valores = df[coluna_destaque].dropna()
quantis = pd.qcut(valores, q=5, labels=False, duplicates="drop")
cmap = cm.get_cmap("viridis")

cores = {}
for nome in df.index:
    if nome in quantis.index:
        idx = quantis[nome]
        cor = mcolors.to_hex(cmap(idx / quantis.max()))
        cores[nome] = cor

# Construção do GeoJSON com propriedades e cor
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

# HTML com filtro integrado no painel lateral
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<style>
  html, body {{
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    display: flex;
    height: 100vh;
    overflow: hidden;
    background-color: #f9fafa;
  }}
  #sidebar {{
    width: 260px;
    background: #fff;
    padding: 20px;
    border-right: 1px solid #ddd;
    box-shadow: 1px 0 4px rgba(0,0,0,0.03);
    display: flex;
    flex-direction: column;
  }}
  #sidebar h2 {{
    margin-bottom: 10px;
    font-size: 18px;
    color: #1a2d5a;
  }}
  #filter {{
    margin-bottom: 12px;
    padding: 8px 10px;
    font-size: 14px;
    border-radius: 8px;
    border: 1px solid #ccc;
  }}
  #search {{
    margin-bottom: 12px;
    padding: 8px 10px;
    font-size: 14px;
    border-radius: 8px;
    border: 1px solid #ccc;
  }}
  #list {{
    flex-grow: 1;
    overflow-y: auto;
  }}
  #list div {{
    padding: 8px 10px;
    margin-bottom: 6px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 15px;
    color: #1a2d5a;
  }}
  #list div:hover {{
    background-color: #e3ecf9;
  }}
  #map {{
    flex-grow: 1;
    position: relative;
  }}
  svg {{
    width: 100%;
    height: 100%;
  }}
  .area {{
    stroke: #4d648d;
    stroke-width: 1;
    transition: 0.3s;
  }}
</style>
</head>
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
    <input id="search" type="text" placeholder="Buscar município..." />
    <div id="list"></div>
  </div>
  <div id="map">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
  </div>
  <script>
    const geo = {geojson_str};
    const svg = document.querySelector("svg");
    const list = document.getElementById("list");

    let coords = [];
    geo.features.forEach(f => {{
      const g = f.geometry;
      if (g.type === "Polygon") g.coordinates[0].forEach(c => coords.push(c));
      else g.coordinates.forEach(p => p[0].forEach(c => coords.push(c)));
    }});
    const lons = coords.map(c => c[0]);
    const lats = coords.map(c => c[1]);
    const minX = Math.min(...lons), maxX = Math.max(...lons);
    const minY = Math.min(...lats), maxY = Math.max(...lats);

    function project([lon, lat]) {{
      const x = ((lon - minX) / (maxX - minX)) * 920 + 40;
      const y = 900 - ((lat - minY) / (maxY - minY)) * 880;
      return [x, y];
    }}

    function polygonToPath(coords) {{
      return coords.map(c => project(c).join(",")).join(" ");
    }}

    geo.features.forEach(f => {{
      const name = f.properties.name;
      let d = "";
      if (f.geometry.type === "Polygon") {{
        d = "M" + polygonToPath(f.geometry.coordinates[0]) + " Z";
      }} else {{
        f.geometry.coordinates.forEach(p => {{
          d += "M" + polygonToPath(p[0]) + " Z ";
        }});
      }}
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", d.trim());
      path.setAttribute("fill", f.properties.color || "#ccc");
      path.classList.add("area");
      svg.appendChild(path);

      const div = document.createElement("div");
      div.textContent = name;
      list.appendChild(div);
    }});
  </script>
</body>
</html>
"""

# Exibe o HTML com o mapa
st.components.v1.html(html_code, height=720, scrolling=False)
