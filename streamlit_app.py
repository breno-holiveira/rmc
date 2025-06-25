import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregando dados
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
  * {{
    margin: 0; padding: 0; box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }}
  html, body, #root, #container {{
    height: 100%; overflow: hidden;
    background: #f7faff;
  }}
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
  /* Painel info refinado */
  #info {{
    position: absolute;
    top: 20px;
    right: 20px;
    background: rgba(255, 255, 255, 0.88);
    backdrop-filter: saturate(180%) blur(10px);
    border-radius: 16px;
    padding: 20px 24px;
    max-width: 260px;
    font-size: 14px;
    color: #1a2d5a;
    box-shadow: 0 8px 20px rgba(0,0,0,0.10);
    display: none;
    user-select: text;
    line-height: 1.4;
    transition: opacity 0.4s ease, transform 0.4s ease;
    opacity: 0;
    transform: translateX(25px);
  }}
  #info.visible {{
    display: block;
    opacity: 1;
    transform: translateX(0);
  }}
  #info h3 {{
    margin-bottom: 16px;
    font-weight: 700;
    font-size: 22px;
    color: #2c3e70;
  }}
  .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 16px;
  }}
  .label {{
    font-weight: 600;
    color: #4d648d;
    white-space: nowrap;
  }}
  .value {{
    text-align: right;
    font-weight: 600;
    color: #2c3e70;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 110px;
  }}
  .value:hover {{
    cursor: help;
    position: relative;
  }}
  /* Tooltip para valores no painel */
  .value:hover::after {{
    content: attr(data-full);
    position: absolute;
    top: 100%;
    right: 0;
    background: rgba(30, 60, 120, 0.9);
    color: white;
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 12px;
    white-space: nowrap;
    margin-top: 4px;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  }}
  .fonte {{
    grid-column: 1 / -1;
    font-size: 10px;
    font-style: italic;
    text-align: right;
    color: #7f8caa;
    margin-top: 14px;
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
        <div class="label">PIB:</div>
        <div class="value" id="pib" data-full=""></div>
        <div class="label">% RMC:</div>
        <div class="value" id="part" data-full=""></div>
        <div class="label">Per capita:</div>
        <div class="value" id="percapita" data-full=""></div>
        <div class="label">População:</div>
        <div class="value" id="pop" data-full=""></div>
        <div class="label">Área:</div>
        <div class="value" id="area" data-full=""></div>
        <div class="label">Densidade:</div>
        <div class="value" id="dens" data-full=""></div>
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

// Coleta todas coordenadas para projeção
const coords = [];
geo.features.forEach(f => {{
  const g = f.geometry;
  if (g.type === "Polygon") g.coordinates[0].forEach(c => coords.push(c));
  else g.coordinates.forEach(p => p[0].forEach(c => coords.push(c)));
}});
const lons = coords.map(c => c[0]), lats = coords.map(c => c[1]);
const minX = Math.min(...lons), maxX = Math.max(...lons);
const minY = Math.min(...lats), maxY = Math.max(...lats);

// Projeta coordenadas geográficas para SVG
function project([lon, lat]) {{
  const x = ((lon - minX) / (maxX - minX)) * 920 + 40;
  const y = 900 - ((lat - minY) / (maxY - minY)) * 880;
  return [x, y];
}}

// Converte array de coordenadas em path SVG
function polygonToPath(coords) {{
  return coords.map(c => project(c).join(",")).join(" ");
}}

// Scroll automático para item ativo na lista lateral
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

// Seleciona município, atualiza destaque e painel info
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

// Preenche painel info e configura tooltips para valores truncados
function showInfo(name) {{
  const f = geo.features.find(f => f.properties.name === name);
  if (!f) return;
  info.classList.add("visible");

  const setVal = (id, val) => {{
    const el = info.querySelector("#" + id);
    if (!el) return;
    if (val === undefined || val === null) val = "-";
    else if(typeof val === "number") {{
      if (id === "part") val = (val * 100).toFixed(2).replace('.', ',') + "%";
      else if (id === "area") val = val.toFixed(2).replace('.', ',') + " km²";
      else if (id === "dens") val = val.toLocaleString("pt-BR") + " hab/km²";
      else val = "R$ " + val.toLocaleString("pt-BR");
    }} else if (typeof val === "string") {{
      val = val;
    }}
    el.textContent = val;
    el.setAttribute("data-full", val);
  }}

  setVal("pib", f.properties.pib_2021);
  setVal("part", f.properties.participacao_rmc);
  setVal("percapita", f.properties.per_capita_2021);
  setVal("pop", f.properties.populacao_2022);
  setVal("area", f.properties.area);
  setVal("dens", f.properties.densidade_demografica_2022);

  info.querySelector("h3").textContent = name;
}}

// Cria os polígonos e itens da lista
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
  div.className = "municipio-item";
  div.setAttribute("role", "option");
  div.tabIndex = 0;
  div.addEventListener("click", () => select(name));
  div.addEventListener("keydown", e => {{
    if(e.key === "Enter" || e.key === " ") {{
      e.preventDefault();
      select(name);
    }}
  }});
  list.appendChild(div);
}});

// Filtra municípios conforme busca
search.addEventListener("input", e => {{
  const val = e.target.value.toLowerCase();
  document.querySelectorAll('.municipio-item').forEach(d => {{
    d.style.display = d.textContent.toLowerCase().includes(val) ? "block" : "none";
  }});
}});

// Seleciona primeiro município na carga
if (geo.features.length > 0) select(geo.features[0].properties.name);
</script>
</body>
</html>
"""

components.html(html_code, height=760, scrolling=False)
