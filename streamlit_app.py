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

# Construção do GeoJSON com dados
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
  html, body {{
    margin: 0; padding: 0; height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f9fafa;
    overflow: hidden;
  }}

  /* Container principal - usa flex */
  body {{
    display: flex;
    height: 100vh;
    width: 100vw;
    gap: 0;
  }}

  /* Sidebar - lista municípios */
  #sidebar {{
    width: 260px;
    background: #fff;
    border-right: 1px solid #e1e4e8;
    box-shadow: 1px 0 5px rgba(0,0,0,0.03);
    display: flex;
    flex-direction: column;
    padding: 16px 14px 10px 14px;
    overflow-y: auto;
  }}
  #sidebar h2 {{
    margin: 0 0 10px 0;
    font-size: 17px;
    font-weight: 600;
    color: #1a2d5a;
    user-select: none;
  }}
  #search {{
    margin-bottom: 12px;
    padding: 7px 12px;
    font-size: 14px;
    border: 1.5px solid #ccc;
    border-radius: 8px;
    outline-offset: 2px;
    transition: border-color 0.3s ease;
  }}
  #search:focus {{
    border-color: #4d648d;
    box-shadow: 0 0 6px rgba(77, 100, 141, 0.55);
  }}
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 6px;
  }}
  #list div {{
    padding: 8px 12px;
    margin-bottom: 5px;
    border-radius: 10px;
    cursor: pointer;
    user-select: none;
    font-size: 15px;
    line-height: 1.4;
    color: #1a2d5a;
    transition: background-color 0.3s ease, color 0.3s ease;
  }}
  #list div:hover {{
    background-color: #e3ecf9;
  }}
  #list div.active {{
    background-color: #4d648d;
    color: #fff;
    font-weight: 700;
  }}

  /* Mapa - ocupa o espaço central */
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

  /* Tooltip */
  #tooltip {{
    position: fixed;
    padding: 5px 11px;
    background: rgba(30, 60, 120, 0.95);
    color: white;
    font-size: 13px;
    border-radius: 5px;
    pointer-events: none;
    display: none;
    box-shadow: 0 0 8px rgba(0,0,0,0.12);
    z-index: 1000;
    user-select: none;
    white-space: nowrap;
  }}

  /* Coluna de info - dados rápidos */
  #info {{
    width: 320px;
    background: #f0f3f8;
    padding: 22px 26px;
    border-radius: 12px 0 0 12px;
    box-shadow: inset 2px 0 6px rgba(0,0,0,0.04);
    font-size: 14px;
    line-height: 1.5;
    color: #1a2d5a;
    user-select: none;
    border-left: 1px solid #d9e2f3;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }}
  #info h3 {{
    margin: 0 0 20px 0;
    font-size: 21px;
    font-weight: 700;
    color: #2c3e70;
    border-bottom: 1px solid #c3d0e8;
    padding-bottom: 8px;
    flex-shrink: 0;
  }}
  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    row-gap: 10px;
    column-gap: 26px;
    flex-grow: 1;
  }}
  #info .label {{
    font-weight: 700;
    color: #4d648d;
    white-space: nowrap;
  }}
  #info .value {{
    font-weight: 600;
    text-align: right;
    color: #34495e;
    white-space: nowrap;
    overflow-wrap: normal;
  }}
  #info .fonte {{
    grid-column: 1 / -1;
    font-size: 11px;
    color: #7f8caa;
    font-style: italic;
    margin-top: 24px;
    text-align: right;
  }}

  /* Scrollbar customizado (opcional) */
  #sidebar::-webkit-scrollbar, #list::-webkit-scrollbar, #info::-webkit-scrollbar {{
    width: 8px;
  }}
  #sidebar::-webkit-scrollbar-thumb, #list::-webkit-scrollbar-thumb, #info::-webkit-scrollbar-thumb {{
    background-color: rgba(77, 100, 141, 0.3);
    border-radius: 4px;
  }}
  #sidebar::-webkit-scrollbar-track, #list::-webkit-scrollbar-track, #info::-webkit-scrollbar-track {{
    background-color: transparent;
  }}
</style>
</head>
<body>
  <div id="sidebar" role="complementary" aria-label="Lista de municípios">
    <h2>Municípios</h2>
    <input id="search" type="search" placeholder="Buscar município..." aria-label="Buscar município" />
    <div id="list" tabindex="0" role="listbox" aria-multiselectable="false" aria-label="Lista de municípios"></div>
  </div>
  <div id="map" role="main" aria-label="Mapa interativo da Região Metropolitana de Campinas">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
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

st.components.v1.html(html_code, height=720, scrolling=False)
