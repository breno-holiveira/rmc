import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregar shapefile e dados
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

# Construção GeoJSON
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
  /* Reset */
  *, *::before, *::after {{
    box-sizing: border-box;
  }}
  html, body {{
    margin: 0; padding: 0;
    height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    font-weight: 300;
    font-size: 16px;
    line-height: 1.6;
    color: #222222;
    background-color: #fff;
    display: flex;
    overflow: hidden;
  }}

  /* Sidebar minimalista */
  #sidebar {{
    width: 280px;
    border-right: 1px solid #ddd;
    background: #fafafa;
    display: flex;
    flex-direction: column;
    padding: 24px 20px 20px 20px;
  }}
  #sidebar h2 {{
    margin: 0 0 24px 0;
    font-weight: 400;
    font-size: 20px;
    letter-spacing: 0.05em;
    color: #444;
  }}
  #search {{
    padding: 10px 14px;
    font-size: 15px;
    border: 1px solid #ccc;
    border-radius: 6px;
    outline-offset: 2px;
    outline-color: #999;
    font-weight: 300;
    transition: outline-color 0.3s ease;
    margin-bottom: 24px;
    color: #333;
  }}
  #search::placeholder {{
    color: #aaa;
    font-style: italic;
  }}
  #search:focus {{
    outline-color: #666;
  }}

  /* Lista limpa */
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 8px;
  }}
  #list::-webkit-scrollbar {{
    width: 6px;
  }}
  #list::-webkit-scrollbar-track {{
    background: #f0f0f0;
  }}
  #list::-webkit-scrollbar-thumb {{
    background: #bbb;
    border-radius: 3px;
  }}
  #list div {{
    padding: 10px 14px;
    margin-bottom: 10px;
    cursor: pointer;
    border-radius: 6px;
    font-weight: 300;
    color: #333;
    user-select: none;
    transition: background-color 0.3s ease, color 0.3s ease;
    border: 1px solid transparent;
  }}
  #list div:hover {{
    background-color: #eee;
    color: #111;
    border-color: #ccc;
  }}
  #list div.active {{
    background-color: #ddd;
    color: #000;
    font-weight: 500;
    border-color: #bbb;
  }}

  /* Área do mapa */
  #map {{
    flex-grow: 1;
    position: relative;
    background: #fff;
    overflow: hidden;
    padding: 20px 40px 20px 40px;
  }}
  svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}

  /* Polígonos simples, linha fina e cor neutra */
  .area {{
    fill: #c8c8c8;
    stroke: #999;
    stroke-width: 1;
    cursor: pointer;
    transition: fill 0.25s ease, stroke-width 0.25s ease;
  }}
  .area:hover {{
    fill: #a0a0a0;
    stroke-width: 1.5;
  }}
  .area.selected {{
    fill: #707070;
    stroke: #555;
    stroke-width: 1.8;
  }}

  /* Tooltip minimalista */
  #tooltip {{
    position: fixed;
    padding: 6px 12px;
    background: rgba(34, 34, 34, 0.85);
    color: #fff;
    font-size: 14px;
    border-radius: 4px;
    pointer-events: none;
    display: none;
    z-index: 1000;
    user-select: none;
    font-weight: 300;
  }}

  /* Painel de informação ultraleve */
  #info {{
    position: fixed;
    right: 28px;
    top: 28px;
    background: #fff;
    border: 1px solid #ddd;
    padding: 20px 28px;
    border-radius: 8px;
    box-shadow: none;
    max-width: 300px;
    font-weight: 300;
    color: #222;
    display: none;
    line-height: 1.5;
    user-select: none;
    z-index: 1100;
  }}
  #info.visible {{
    display: block;
  }}
  #info h3 {{
    margin-top: 0;
    margin-bottom: 18px;
    font-weight: 400;
    font-size: 22px;
    letter-spacing: 0.04em;
    color: #111;
  }}
  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    row-gap: 12px;
    column-gap: 18px;
  }}
  #info .label {{
    font-weight: 400;
    color: #555;
    white-space: nowrap;
  }}
  #info .value {{
    font-weight: 300;
    text-align: right;
    color: #111;
    white-space: nowrap;
    font-variant-numeric: tabular-nums;
  }}
  #info .fonte {{
    grid-column: 1 / -1;
    font-size: 12px;
    font-style: italic;
    color: #888;
    margin-top: 20px;
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

st.components.v1.html(html_code, height=620, scrolling=False)
