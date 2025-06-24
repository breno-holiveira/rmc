import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Dados shapefile
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

<!-- Fonte Inter do Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">

<style>
  /* Reset e base */
  *, *::before, *::after {{
    box-sizing: border-box;
  }}
  html, body {{
    margin: 0; padding: 0;
    height: 100vh;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    font-weight: 300;
    font-size: 16px;
    line-height: 1.5;
    color: #222;
    background: linear-gradient(145deg, #f7f9fc 0%, #e8edf3 100%);
    display: flex;
    overflow: hidden;
  }}

  /* Sidebar refinada */
  #sidebar {{
    width: 280px;
    background: linear-gradient(180deg, #ffffffcc 0%, #f0f4fcdd 100%);
    border-right: 1px solid #c1c9d4;
    box-shadow: 2px 0 8px rgba(140, 150, 180, 0.1);
    display: flex;
    flex-direction: column;
    padding: 28px 22px 22px 22px;
    user-select: none;
  }}
  #sidebar h2 {{
    margin: 0 0 28px 0;
    font-weight: 600;
    font-size: 22px;
    letter-spacing: 0.06em;
    color: #34415e;
    text-transform: uppercase;
  }}
  #search {{
    padding: 12px 16px;
    font-size: 15px;
    border-radius: 8px;
    border: 1.8px solid #9ea9ba;
    background: #fafbfc;
    color: #4a5060;
    font-weight: 400;
    outline-offset: 3px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 28px;
  }}
  #search::placeholder {{
    color: #9fa7b3;
    font-style: italic;
  }}
  #search:focus {{
    border-color: #5773ff;
    box-shadow: 0 0 6px rgba(87, 115, 255, 0.45);
    background: #ffffff;
  }}

  /* Lista de municípios */
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 8px;
    scrollbar-width: thin;
    scrollbar-color: #a2aecb transparent;
  }}
  #list::-webkit-scrollbar {{
    width: 8px;
  }}
  #list::-webkit-scrollbar-track {{
    background: transparent;
  }}
  #list::-webkit-scrollbar-thumb {{
    background: #a2aecb;
    border-radius: 5px;
  }}
  #list div {{
    padding: 12px 16px;
    margin-bottom: 12px;
    font-weight: 400;
    color: #3b4563;
    cursor: pointer;
    border-radius: 10px;
    user-select: none;
    transition: background-color 0.25s ease, color 0.25s ease, box-shadow 0.3s ease;
    border: 1px solid transparent;
    box-shadow: inset 0 0 0 0 transparent;
  }}
  #list div:hover {{
    background-color: #e5eaff;
    color: #2f3c7e;
    border-color: #7b8de0;
    box-shadow: inset 3px 0 8px rgba(123, 141, 224, 0.3);
  }}
  #list div.active {{
    background-color: #5773ff;
    color: #fff;
    font-weight: 600;
    border-color: #4665db;
    box-shadow: 0 0 12px rgba(87, 115, 255, 0.8);
  }}

  /* Mapa */
  #map {{
    flex-grow: 1;
    position: relative;
    padding: 28px 48px;
    background: #fff;
    border-radius: 18px 0 0 18px;
    box-shadow: 0 8px 18px rgba(61, 78, 125, 0.15);
    overflow: hidden;
  }}
  svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}

  /* Polígonos */
  .area {{
    fill: #b7c3e3;
    stroke: #5773ff;
    stroke-width: 1.3;
    cursor: pointer;
    transition: fill 0.3s ease, stroke-width 0.3s ease, filter 0.3s ease;
    filter: drop-shadow(0 0 0 transparent);
  }}
  .area:hover {{
    fill: #4e63b9;
    stroke-width: 2.3;
    filter: drop-shadow(0 0 6px rgba(87, 115, 255, 0.35));
  }}
  .area.selected {{
    fill: #2f3c7e;
    stroke: #1b264f;
    stroke-width: 2.8;
    filter: drop-shadow(0 0 10px rgba(46, 57, 111, 0.6));
  }}

  /* Tooltip elegante */
  #tooltip {{
    position: fixed;
    padding: 8px 16px;
    background: rgba(41, 48, 78, 0.85);
    color: #edf1f7;
    font-size: 14px;
    border-radius: 12px;
    pointer-events: none;
    display: none;
    user-select: none;
    font-weight: 500;
    box-shadow: 0 0 12px rgba(41, 48, 78, 0.65);
    z-index: 1100;
  }}

  /* Painel info */
  #info {{
    position: fixed;
    right: 36px;
    top: 36px;
    max-width: 360px;
    background: linear-gradient(145deg, #f4f7ff, #dce4fb);
    border-radius: 20px;
    padding: 28px 32px;
    box-shadow: 0 14px 38px rgba(31, 48, 75, 0.15);
    color: #2c3459;
    font-weight: 400;
    font-size: 15px;
    line-height: 1.5;
    user-select: none;
    display: none;
    border: 1px solid #a2a9bf;
    backdrop-filter: saturate(180%) blur(10px);
    -webkit-backdrop-filter: saturate(180%) blur(10px);
    transition: opacity 0.3s ease;
    z-index: 1200;
  }}
  #info.visible {{
    display: block;
    opacity: 1;
  }}
  #info h3 {{
    margin: 0 0 24px 0;
    font-weight: 600;
    font-size: 24px;
    letter-spacing: 0.04em;
    color: #1b2341;
  }}
  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px 26px;
  }}
  #info .label {{
    font-weight: 600;
    color: #465387;
    white-space: nowrap;
  }}
  #info .value {{
    font-weight: 500;
    text-align: right;
    font-variant-numeric: tabular-nums;
    color: #2c3459;
    white-space: nowrap;
  }}
  #info .fonte {{
    grid-column: 1 / -1;
    font-style: italic;
    font-weight: 300;
    font-size: 13px;
    color: #6872a0;
    margin-top: 24px;
    text-align: right;
  }}

</style>
</head>
<body>
  <div id="sidebar" role="complementary" aria-label="Lista de municípios">
    <h2>Municípios</h2>
    <input id="search" type="search" placeholder="Buscar município..." aria-label="Buscar município" autocomplete="off" />
    <div id="list" tabindex="0" role="listbox" aria-multiselectable="false" aria-label="Lista de municípios"></div>
  </div>

  <div id="map" role="main" aria-label="Mapa interativo da Região Metropolitana de Campinas">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" aria-hidden="true"></svg>
    <div id="tooltip" role="tooltip" aria-hidden="true"></div>
  </div>

  <div id="info" role="region" aria-live="polite" aria-label="Informações do município selecionado">
    <h3>Município</h3>
    <div class="grid">
      <div class="label">PIB 2021:</div> <div class="value" id="pib"></div>
      <div class="label">% no PIB regional:</div> <div class="value" id="part"></div>
      <div class="label">PIB per capita (2021):</div> <div class="value" id="percapita"></div>
      <div class="label">População (2022):</div> <div class="value" id="pop"></div>
      <div class="label">Área:</div> <div class="value" id="area"></div>
      <div class="label">Densidade demográfica:</div> <div class="value" id="dens"></div>
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
  }}
  selected = name;
  if (paths[name]) {{
    paths[name].classList.add("selected");
    [...list.children].forEach(div => {{
      if(div.dataset.name === name) {{
        div.classList.add("active");
        const container = list;
        const containerHeight = container.clientHeight;
        const containerTop = container.getBoundingClientRect().top;
        const elementTop = div.getBoundingClientRect().top;
        const elementHeight = div.offsetHeight;
        const scrollTop = container.scrollTop;
        const offset = elementTop - containerTop;
        const scrollTo = scrollTop + offset - containerHeight / 2 + elementHeight / 2;
        container.scrollTo({{ top: scrollTo, behavior: "smooth" }});
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
    if(div.textContent.toLowerCase().includes(filterLower)) {{
      div.style.display = "block";
    }} else {{
      div.style.display = "none";
    }}
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
    const offsetX = 8;
    const offsetY = -22;
    tooltip.style.left = (e.clientX + offsetX) + "px";
    tooltip.style.top = (e.clientY + offsetY) + "px";
    tooltip.style.display = "block";
    tooltip.textContent = name;
  }});
  path.addEventListener("mouseleave", () => {{
    tooltip.style.display = "none";
  }});
  path.addEventListener("click", e => {{
    e.preventDefault();
    e.stopPropagation();
    select(name);
  }});

  const div = document.createElement("div");
  div.textContent = name;
  div.dataset.name = name;
  div.tabIndex = 0;
  div.setAttribute('role', 'option');
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
  updateList(e.target.value);
  const visibleItems = [...list.children].filter(d => d.style.display !== "none");
  if(visibleItems.length === 1) {{
    select(visibleItems[0].dataset.name);
  }}
}});

if(geo.features.length > 0) {{
  select(geo.features[0].properties.name);
}}
</script>

</body>
</html>
"""

st.components.v1.html(html_code, height=660, scrolling=False)
