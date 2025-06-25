import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregamento de dados
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

# Montagem do GeoJSON
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

# HTML responsivo com ajustes visuais refinados
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Mapa Interativo RMC</title>
<style>
  body {{
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    background: #f8f9fa;
    display: flex;
    height: 100vh;
    overflow: hidden;
  }}
  #sidebar {{
    width: 240px;
    background: #fff;
    padding: 16px;
    border-right: 1px solid #ddd;
    box-shadow: 1px 0 3px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
  }}
  #sidebar h2 {{
    margin: 0 0 10px;
    font-size: 17px;
    color: #1a2d5a;
  }}
  #search {{
    padding: 8px 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 6px;
    margin-bottom: 12px;
  }}
  #list {{
    overflow-y: auto;
    flex-grow: 1;
  }}
  #list div {{
    padding: 8px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
    font-size: 14px;
    color: #333;
  }}
  #list div:hover {{
    background: #eef3fb;
  }}
  #list div.active {{
    background: #2c3e70;
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
    fill: #acc7e6;
    stroke: #34495e;
    stroke-width: 1;
    cursor: pointer;
    transition: 0.3s ease;
  }}
  .area:hover {{
    fill: #90b0d9;
    stroke-width: 1.5;
  }}
  .area.selected {{
    fill: #2c3e70;
  }}
  #tooltip {{
    position: fixed;
    background: rgba(44, 62, 112, 0.95);
    color: #fff;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 12px;
    display: none;
    pointer-events: none;
    z-index: 1000;
  }}
  #info {{
    position: absolute;
    top: 24px;
    right: 24px;
    background: #fff;
    padding: 16px 20px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    font-size: 13px;
    line-height: 1.5;
    max-width: 280px;
    display: none;
    z-index: 10;
  }}
  #info.visible {{
    display: block;
  }}
  #info h3 {{
    margin-top: 0;
    font-size: 16px;
    color: #2c3e70;
    margin-bottom: 8px;
  }}
  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 16px;
  }}
  #info .label {{
    font-weight: 600;
    color: #4d648d;
  }}
  #info .value {{
    text-align: right;
    color: #2d3f54;
  }}
  #info .fonte {{
    font-size: 10px;
    color: #7a8ba3;
    margin-top: 10px;
    text-align: right;
    grid-column: 1 / -1;
  }}
</style>
</head>
<body>
<div id="sidebar">
  <h2>Municípios</h2>
  <input id="search" type="search" placeholder="Buscar município..." />
  <div id="list"></div>
</div>
<div id="map">
  <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
  <div id="tooltip"></div>
  <div id="info">
    <h3>Município</h3>
    <div class="grid">
      <div class="label">PIB 2021:</div><div class="value" id="pib"></div>
      <div class="label">% no PIB regional:</div><div class="value" id="part"></div>
      <div class="label">PIB per capita:</div><div class="value" id="percapita"></div>
      <div class="label">População (2022):</div><div class="value" id="pop"></div>
      <div class="label">Área:</div><div class="value" id="area"></div>
      <div class="label">Densidade:</div><div class="value" id="dens"></div>
      <div class="fonte">Fonte: IBGE Cidades</div>
    </div>
  </div>
</div>
<script>
const geo = {geojson_str};
const svg = document.querySelector("svg");
const tooltip = document.getElementById("tooltip");
const info = document.getElementById("info");
const list = document.getElementById("list");
const search = document.getElementById("search");
const paths = {{}};
let selected = null;

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
function select(name) {{
  if (selected) {{
    paths[selected].classList.remove("selected");
    [...list.children].forEach(d => d.classList.remove("active"));
  }}
  selected = name;
  if (paths[name]) {{
    paths[name].classList.add("selected");
    [...list.children].forEach(div => {{
      if(div.dataset.name === name) {{
        div.classList.add("active");
      }}
    }});
    showInfo(name);
  }}
}}
function showInfo(name) {{
  const f = geo.features.find(f => f.properties.name === name);
  if (!f) return;
  info.querySelector("h3").textContent = name;
  info.querySelector("#pib").textContent = f.properties.pib_2021 ? "R$ " + f.properties.pib_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace('.', ',') + "%" : "-";
  info.querySelector("#percapita").textContent = f.properties.per_capita_2021 ? "R$ " + f.properties.per_capita_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#pop").textContent = f.properties.populacao_2022 ? f.properties.populacao_2022.toLocaleString("pt-BR") : "-";
  info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace(".", ",") + " km²" : "-";
  info.querySelector("#dens").textContent = f.properties.densidade_demografica_2022 ? f.properties.densidade_demografica_2022.toLocaleString("pt-BR") + " hab/km²" : "-";
  info.classList.add("visible");
}}
function updateList(filter = "") {{
  const filterLower = filter.toLowerCase();
  [...list.children].forEach(div => {{
    div.style.display = div.textContent.toLowerCase().includes(filterLower) ? "block" : "none";
  }});
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
  path.classList.add("area");
  path.setAttribute("data-name", name);
  svg.appendChild(path);
  paths[name] = path;

  path.addEventListener("mousemove", e => {{
    tooltip.style.left = (e.clientX + 10) + "px";
    tooltip.style.top = (e.clientY - 20) + "px";
    tooltip.textContent = name;
    tooltip.style.display = "block";
  }});
  path.addEventListener("mouseleave", () => tooltip.style.display = "none");
  path.addEventListener("click", () => select(name));

  const div = document.createElement("div");
  div.textContent = name;
  div.dataset.name = name;
  div.addEventListener("click", () => select(name));
  list.appendChild(div);
}});
search.addEventListener("input", e => {{
  updateList(e.target.value);
}});
if (geo.features.length > 0) {{
  select(geo.features[0].properties.name);
}}
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=700, scrolling=False)
