import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregar shapefile e dados Excel
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

html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Mapa Interativo RMC</title>
<style>
  /* Reset e base */
  * {{ margin:0; padding:0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
  html, body, #root, #container {{ height: 100%; overflow: hidden; background: #f7faff; }}

  #container {{
    display: flex;
    height: 100vh;
    width: 100vw;
    user-select: none;
  }}

  /* Sidebar */
  #sidebar {{
    width: 280px;
    background: #fff;
    border-right: 1px solid #cbd3db;
    display: flex;
    flex-direction: column;
    padding: 16px 18px;
    overflow-y: auto;
  }}
  #search {{
    padding: 8px 12px;
    border: 1px solid #a9b6cd;
    border-radius: 8px;
    font-size: 14px;
    margin-bottom: 12px;
    outline-offset: 2px;
    transition: border-color 0.3s ease;
  }}
  #search:focus {{
    border-color: #4d648d;
    box-shadow: 0 0 6px rgba(77,100,141,0.5);
  }}

  #municipio-list {{
    flex-grow: 1;
    overflow-y: auto;
  }}
  .municipio-item {{
    padding: 8px 10px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
    color: #1a2d5a;
    margin-bottom: 6px;
    transition: background-color 0.25s, color 0.25s;
  }}
  .municipio-item:hover {{
    background-color: #d3e0f7;
  }}
  .municipio-item.active {{
    background-color: #4d648d;
    color: #fff;
    font-weight: 600;
  }}

  /* Área mapa */
  #map-area {{
    flex-grow: 1;
    position: relative;
    background: #e6f0ff;
    display: flex;
    flex-direction: column;
  }}

  svg {{
    width: 100%;
    height: calc(100vh - 40px);
    display: block;
  }}

  .area {{
    fill: #b6cce5;
    stroke: #4d648d;
    stroke-width: 1;
    cursor: pointer;
    transition: fill 0.3s ease, stroke-width 0.3s ease;
  }}
  .area:hover {{
    fill: #8db3dd;
    stroke-width: 1.5;
  }}
  .area.selected {{
    fill: #4d648d;
    stroke: #1a2d5a;
  }}

  /* Tooltip */
  #tooltip {{
    position: absolute;
    background: rgba(30, 60, 120, 0.9);
    color: white;
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 13px;
    pointer-events: none;
    display: none;
    white-space: nowrap;
    z-index: 999;
  }}

  /* Painel info */
  #info {{
    position: absolute;
    top: 20px;
    right: 20px;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: saturate(180%) blur(8px);
    border-radius: 14px;
    padding: 18px 22px;
    max-width: 260px;
    font-size: 14px;
    color: #1a2d5a;
    box-shadow: 0 4px 15px rgba(0,0,0,0.12);
    display: none;
    user-select: text;
    line-height: 1.3;
    transition: opacity 0.35s ease, transform 0.35s ease;
    opacity: 0;
    transform: translateX(20px);
  }}
  #info.visible {{
    display: block;
    opacity: 1;
    transform: translateX(0);
  }}
  #info h3 {{
    margin-bottom: 14px;
    font-weight: 700;
    font-size: 20px;
  }}
  .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 18px;
  }}
  .label {{
    font-weight: 600;
    color: #4d648d;
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
    font-style: italic;
    text-align: right;
    color: #7f8caa;
    margin-top: 12px;
  }}

</style>
</head>
<body>
<div id="container" role="main" aria-label="Mapa interativo da Região Metropolitana de Campinas">
  <aside id="sidebar" role="complementary" aria-label="Lista de municípios">
    <input type="search" id="search" aria-label="Buscar município" placeholder="Buscar município..." autocomplete="off" />
    <div id="municipio-list" tabindex="0" role="listbox" aria-multiselectable="false" aria-label="Lista de municípios"></div>
  </aside>
  <section id="map-area">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" aria-label="Mapa dos municípios"></svg>
    <div id="tooltip" role="tooltip" aria-hidden="true"></div>
    <section id="info" role="region" aria-live="polite" aria-label="Informações do município selecionado">
      <h3>Município</h3>
      <div class="grid">
        <div class="label">PIB:</div><div class="value" id="pib"></div>
        <div class="label">% RMC:</div><div class="value" id="part"></div>
        <div class="label">Per capita:</div><div class="value" id="percapita"></div>
        <div class="label">População:</div><div class="value" id="pop"></div>
        <div class="label">Área:</div><div class="value" id="area"></div>
        <div class="label">Densidade:</div><div class="value" id="dens"></div>
        <div class="fonte">Fonte: IBGE Cidades</div>
      </div>
    </section>
  </section>
</div>

<script>
const geo = {geojson_str};
const svg = document.querySelector("svg");
const tooltip = document.getElementById("tooltip");
const info = document.getElementById("info");
const list = document.getElementById("municipio-list");
const search = document.getElementById("search");
const paths = {{}};
let selected = null;

const coords = [];
geo.features.forEach(f => {{
  const g = f.geometry;
  if (g.type === "Polygon") g.coordinates[0].forEach(c => coords.push(c));
  else g.coordinates.forEach(p => p[0].forEach(c => coords.push(c)));
}});
const lons = coords.map(c => c[0]), lats = coords.map(c => c[1]);
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

function scrollToActive() {{
  const active = document.querySelector('.municipio-item.active');
  if (!active) return;
  const container = list;
  const containerRect = container.getBoundingClientRect();
  const activeRect = active.getBoundingClientRect();
  const offset = activeRect.top - containerRect.top;
  const scrollTop = container.scrollTop;
  const scrollTarget = scrollTop + offset - container.clientHeight/2 + active.clientHeight/2;
  container.scrollTo({{ top: scrollTarget, behavior: "smooth" }});
}}

function select(name) {{
  if (selected) {{
    paths[selected].classList.remove("selected");
    document.querySelectorAll('.municipio-item').forEach(d => d.classList.remove('active'));
  }}
  selected = name;
  if (paths[name]) {{
    paths[name].classList.add("selected");
    showInfo(name);
    const el = document.querySelector(`[data-name="${{name}}"]`);
    if (el) {{
      el.classList.add('active');
      scrollToActive();
    }}
  }}
}}

function showInfo(name) {{
  const f = geo.features.find(f => f.properties.name === name);
  if (!f) return;
  info.classList.add("visible");
  info.querySelector("#pib").textContent = f.properties.pib_2021 ? "R$ " + f.properties.pib_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace('.', ',') + "%" : "-";
  info.querySelector("#percapita").textContent = f.properties.per_capita_2021 ? "R$ " + f.properties.per_capita_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#pop").textContent = f.properties.populacao_2022 ? f.properties.populacao_2022.toLocaleString("pt-BR") : "-";
  info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace('.', ',') + " km²" : "-";
  info.querySelector("#dens").textContent = f.properties.densidade_demografica_2022 ? f.properties.densidade_demografica_2022.toLocaleString("pt-BR") + " hab/km²" : "-";
}}

geo.features.forEach(f => {{
  const name = f.properties.name;
  let d = "";
  if (f.geometry.type === "Polygon") d = "M" + polygonToPath(f.geometry.coordinates[0]) + " Z";
  else f.geometry.coordinates.forEach(p => {{ d += "M" + polygonToPath(p[0]) + " Z "; }});
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", d.trim());
  path.classList.add("area");
  path.setAttribute("data-name", name);
  svg.appendChild(path);
  paths[name] = path;
  path.addEventListener("mousemove", e => {{
    tooltip.style.left = e.clientX + 10 + "px";
    tooltip.style.top = e.clientY - 25 + "px";
    tooltip.textContent = name;
    tooltip.style.display = "block";
  }});
  path.addEventListener("mouseleave", () => {{
    tooltip.style.display = "none";
  }});
  path.addEventListener("click", () => select(name));

  const div = document.createElement("div");
  div.textContent = name;
  div.dataset.name = name;
  div.className = 'municipio-item';
  div.setAttribute("role", "option");
  div.tabIndex = 0;
  div.addEventListener("click", () => select(name));
  div.addEventListener("keydown", e => {{
    if (e.key === "Enter" || e.key === " ") {{
      e.preventDefault();
      select(name);
    }}
  }});
  list.appendChild(div);
}});

search.addEventListener("input", e => {{
  const val = e.target.value.toLowerCase();
  document.querySelectorAll('.municipio-item').forEach(d => {{
    d.style.display = d.textContent.toLowerCase().includes(val) ? 'block' : 'none';
  }});
}});

// Seleciona o primeiro município inicialmente
if (geo.features.length > 0) select(geo.features[0].properties.name);

</script>
</body>
</html>
"""

components.html(html_code, height=760, scrolling=False)
