import streamlit as st
import pandas as pd
import geopandas as gpd
import json

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

# Construção do GeoJSON
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

# HTML/CSS/JS
html_code = f"""
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
    padding: 16px 12px 8px 12px;
    border-right: 1px solid #e1e4e8;
    box-shadow: 1px 0 5px rgba(0,0,0,0.03);
    display: flex;
    flex-direction: column;
    z-index: 10;
  }}
  #sidebar h2 {{
    margin: 0 0 6px 0;
    font-size: 16px;
    font-weight: 600;
    color: #1a2d5a;
  }}
  #search {{
    margin-bottom: 10px;
    padding: 6px 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 8px;
    outline: none;
  }}
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 4px;
  }}
  #list div {{
    padding: 6px 10px;
    margin-bottom: 4px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
    color: #1a2d5a;
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
    overflow: hidden;
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
    fill: #4d648d;
    stroke: #1a2d5a;
  }}

  #tooltip {{
    position: fixed;
    padding: 5px 10px;
    background: rgba(30, 60, 120, 0.95);
    color: white;
    font-size: 13px;
    border-radius: 5px;
    pointer-events: none;
    display: none;
    z-index: 1000;
  }}

  #info {{
    position: absolute;
    right: 0;
    top: 0;
    width: 300px;
    height: 100%;
    background: #f0f3f8;
    padding: 20px;
    border-left: 1px solid #d9e2f3;
    box-shadow: -2px 0 6px rgba(0,0,0,0.06);
    transform: translateX(100%);
    transition: transform 0.4s ease, opacity 0.4s ease;
    opacity: 0;
    pointer-events: none;
    z-index: 20;
  }}
  #info.visible {{
    transform: translateX(0);
    opacity: 1;
    pointer-events: auto;
  }}
  #info h3 {{
    margin-top: 0;
    font-size: 18px;
    color: #2c3e70;
    margin-bottom: 12px;
    border-bottom: 1px solid #c3d0e8;
    padding-bottom: 4px;
  }}
  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    row-gap: 6px;
    column-gap: 20px;
    opacity: 0;
    transition: opacity 0.4s ease;
  }}
  #info.visible .grid {{
    opacity: 1;
  }}
  .label {{
    font-weight: 600;
    color: #4d648d;
    white-space: nowrap;
  }}
  .value {{
    text-align: right;
    font-weight: 500;
    color: #34495e;
    white-space: nowrap;
  }}
  .fonte {{
    grid-column: 1 / -1;
    font-size: 10px;
    color: #7f8caa;
    margin-top: 12px;
    text-align: right;
    font-style: italic;
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
</div>

<div id="info">
  <h3>Município</h3>
  <div class="grid">
    <div class="label">PIB 2021:</div> <div class="value" id="pib"></div>
    <div class="label">% no PIB regional:</div> <div class="value" id="part"></div>
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
  info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace(".", ",") + "%" : "-";
  info.querySelector("#percapita").textContent = f.properties.per_capita_2021 ? "R$ " + f.properties.per_capita_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#pop").textContent = f.properties.populacao_2022 ? f.properties.populacao_2022.toLocaleString("pt-BR") : "-";
  info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace(".", ",") + " km²" : "-";
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
