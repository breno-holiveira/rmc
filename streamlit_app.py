# Gerar novamente o conteúdo do arquivo `streamlit_app.py` completo para Breno colar diretamente

codigo_completo = """
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np

# Configurações da página
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

# Variável escolhida para destaque visual
coluna_destaque = "per_capita_2021"  # Você pode mudar para outras: pib_2021, populacao_2022 etc.

# Normalização por quantis para melhor distribuição de cores
valores = df[coluna_destaque].dropna()
quantis = pd.qcut(valores, q=5, labels=False, duplicates="drop")
cmap = cm.get_cmap("viridis")

cores = {}
for nome in df.index:
    if nome in quantis.index:
        idx = quantis[nome]
        cor = mcolors.to_hex(cmap(idx / quantis.max()))
        cores[nome] = cor

# Construção do GeoJSON com dados e cores
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    props["color"] = cores.get(nome, "#b6cce5")  # Cor padrão caso não tenha
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

# Código HTML com filtro embutido e painel lateral
html_code = f\"\"\"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Mapa Interativo RMC</title>
<style>
  html, body {{
    height: 100vh;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    background-color: #f9fafa;
    display: flex;
    overflow: hidden;
  }}
  #sidebar {{
    width: 260px;
    background: #fff;
    padding: 20px 16px 12px 16px;
    border-right: 1px solid #e1e4e8;
    box-shadow: 1px 0 5px rgba(0,0,0,0.03);
    display: flex;
    flex-direction: column;
  }}
  #sidebar h2 {{
    margin: 0 0 8px 0;
    font-size: 18px;
    font-weight: 600;
    color: #1a2d5a;
  }}
  #filter {{
    margin-bottom: 12px;
    padding: 8px 12px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 8px;
  }}
  #search {{
    margin-bottom: 12px;
    padding: 8px 12px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 8px;
  }}
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 6px;
  }}
  #list div {{
    padding: 8px 12px;
    margin-bottom: 6px;
    border-radius: 8px;
    cursor: pointer;
    user-select: none;
    font-size: 15px;
    color: #1a2d5a;
    transition: background-color 0.3s, color 0.3s;
  }}
  #list div:hover {{
    background-color: #e3ecf9;
  }}
  #list div.active {{
    background-color: #4d648d;
    color: #fff;
    font-weight: 600;
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
    fill: #b6cce5;
    stroke: #4d648d;
    stroke-width: 1;
    cursor: pointer;
    transition: all 0.3s ease;
  }}
  .area:hover {{
    fill: #8db3dd;
    stroke-width: 1.5;
  }}
  .area.selected {{
    stroke: #1a2d5a;
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
    <input id="search" type="search" placeholder="Buscar município..." />
    <div id="list"></div>
  </div>
  <div id="map">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
  </div>
  <script>
    const geo = {geojson_str};
    const svg = document.querySelector("svg");
    const list = document.getElementById("list");
    const paths = {{}};

    function project([lon, lat]) {{
      const lons = geo.features.flatMap(f => f.geometry.coordinates.flat(2).map(c => c[0]));
      const lats = geo.features.flatMap(f => f.geometry.coordinates.flat(2).map(c => c[1]));
      const minX = Math.min(...lons), maxX = Math.max(...lons);
      const minY = Math.min(...lats), maxY = Math.max(...lats);
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
      path.setAttribute("fill", f.properties.color || "#b6cce5");
      path.classList.add("area");
      svg.appendChild(path);
      paths[name] = path;

      const div = document.createElement("div");
      div.textContent = name;
      div.dataset.name = name;
      list.appendChild(div);
    }});
  </script>
</body>
</html>
\"\"\"

st.components.v1.html(html_code, height=720, scrolling=False)
"""

# Salva novamente o código pronto para colar
codigo_path = Path("/mnt/data/streamlit_app_completo.py")
codigo_path.write_text(codigo_completo)
codigo_path

