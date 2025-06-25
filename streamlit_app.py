import streamlit as st
import pandas as pd
import geopandas as gpd
import json

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

features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

# HTML + CSS + JS com painel flutuante transparente e responsivo
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>RMC Interativo</title>
<style>
  html, body {{
    margin: 0;
    padding: 0;
    height: 100vh;
    font-family: 'Segoe UI', sans-serif;
    display: flex;
    overflow: hidden;
    background: #f4f6f9;
  }}

  #sidebar {{
    width: 260px;
    background: #ffffff;
    border-right: 1px solid #ddd;
    padding: 16px;
    box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    z-index: 10;
    overflow-y: auto;
  }}

  #sidebar h2 {{
    font-size: 16px;
    margin-bottom: 8px;
    color: #1a2d5a;
  }}

  #search {{
    width: 100%;
    padding: 6px 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-bottom: 10px;
  }}

  #list {{
    max-height: calc(100vh - 120px);
    overflow-y: auto;
  }}

  #list div {{
    padding: 6px 10px;
    margin-bottom: 6px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s;
  }}

  #list div:hover {{
    background: #e7eefb;
  }}

  #list div.active {{
    background: #4d648d;
    color: #fff;
    font-weight: bold;
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
    fill: #c6d7f2;
    stroke: #4d648d;
    stroke-width: 1;
    cursor: pointer;
    transition: fill 0.2s;
  }}

  .area:hover {{
    fill: #9ebde2;
  }}

  .area.selected {{
    fill: #4d648d;
    stroke: #2b3b66;
  }}

  #tooltip {{
    position: fixed;
    padding: 5px 10px;
    background: #2a3f7c;
    color: white;
    font-size: 13px;
    border-radius: 6px;
    display: none;
    z-index: 1000;
    pointer-events: none;
  }}

  #info {{
    position: absolute;
    top: 30px;
    right: 30px;
    min-width: 280px;
    max-width: 320px;
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    padding: 20px;
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.4s ease;
    pointer-events: none;
    z-index: 20;
  }}

  #info.visible {{
    opacity: 1;
    transform: translateY(0);
    pointer-events: auto;
  }}

  #info h3 {{
    margin-top: 0;
    font-size: 18px;
    color: #1a2d5a;
    border-bottom: 1px solid #ccc;
    padding-bottom: 6px;
    margin-bottom: 12px;
  }}

  .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 20px;
  }}

  .label {{
    font-weight: 600;
    color: #3e4a66;
    white-space: nowrap;
  }}

  .value {{
    text-align: right;
    font-weight: 500;
    color: #2c3e70;
    white-space: nowrap;
  }}

  .fonte {{
    grid-column: 1 / -1;
    font-size: 10px;
    color: #7f8caa;
    text-align: right;
    margin-top: 10px;
    font-style: italic;
  }}
</style>
</head>
<body>
<div id="sidebar">
  <h2>Municípios</h2>
  <input id="search" type="text" placeholder="Buscar..." />
  <div id="list"></div>
</div>

<div id="map">
  <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
  <div id="tooltip"></div>
</div>

<div id="info">
  <h3>Município</h3>
  <div class="grid">
    <div class="label">PIB 2021:</div> <div class="value" id="pib"></div>
    <div class="label">% PIB regional:</div> <div class="value" id="part"></div>
    <div class="label">PIB per capita:</div> <div class="value" id="percapita"></div>
    <div class="label">População:</div> <div class="value" id="pop"></div>
    <div class="label">Área:</div> <div class="value" id="area"></div>
    <div class="label">Densidade:</div> <div class="value" id="dens"></div>
    <div class="fonte">Fonte: IBGE Cidades</div>
  </div>
</div>

<script>
const geo = {geojson_str};
const svg = document.querySelector("svg");
const tooltip = document.getElementById("tooltip");
const info = document.getElementById("info");
const list = document.getElementById("list");
const search = document.getElementById("search");
let selected = null;
const paths = {{}};

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
    info.classList.remove("visible");
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
  info.classList.add("visible");
  info.querySelector("h3").textContent = name;
  info.querySelector("#pib").textContent = f.properties.pib_2021 ? "R$ " + f.properties.pib_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace('.', ',') + "%" : "-";
  info.querySelector("#percapita").textContent = f.properties.per_capita_2021 ? "R$ " + f.properties.per_capita_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#pop").textContent = f.properties.populacao_2022 ? f.properties.populacao_2022.toLocaleString("pt-BR") : "-";
  info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace('.', ',') + " km²" : "-";
  info.querySelector("#dens").textContent = f.properties.densidade_demografica_2022 ? f.properties.densidade_demografica_2022.toLocaleString("pt-BR") + " hab/km²" : "-";
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
    tooltip.style.display = "block";
    tooltip.textContent = name;
  }});
  path.addEventListener("mouseleave", () => tooltip.style.display = "none");
  path.addEventListener("click", e => {{
    e.preventDefault();
    e.stopPropagation();
    select(name);
  }});

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

st.components.v1.html(html_code, height=750, scrolling=False)
