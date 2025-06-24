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
  /* Reset */
  * {{
    box-sizing: border-box;
  }}
  html, body {{
    height: 100vh;
    margin: 0; padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, rgba(250,250,252,0.95) 0%, rgba(230,235,240,0.9) 100%);
    display: flex;
    overflow: hidden;
    color: #1a2d5a;
    user-select: none;
  }}

  /* Sidebar transparente e minimalista */
  #sidebar {{
    width: 280px;
    background: rgba(255 255 255 / 0.12);
    backdrop-filter: saturate(180%) blur(16px);
    -webkit-backdrop-filter: saturate(180%) blur(16px);
    border-right: 1px solid rgba(255 255 255 / 0.15);
    padding: 20px 18px 16px 18px;
    display: flex;
    flex-direction: column;
    box-shadow: inset 0 0 30px rgba(255 255 255 / 0.25);
  }}
  #sidebar h2 {{
    margin: 0 0 14px 0;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #2a3a72;
  }}
  #search {{
    margin-bottom: 14px;
    padding: 10px 14px;
    font-size: 15px;
    border-radius: 12px;
    border: 1.5px solid rgba(255 255 255 / 0.4);
    background: rgba(255 255 255 / 0.18);
    color: #283556;
    outline-offset: 3px;
    transition:
      background-color 0.3s ease,
      border-color 0.4s ease,
      box-shadow 0.4s ease;
    font-weight: 500;
  }}
  #search::placeholder {{
    color: #aac0e2;
    font-style: italic;
  }}
  #search:focus {{
    background-color: rgba(255 255 255 / 0.28);
    border-color: #4662b8;
    box-shadow: 0 0 8px rgba(70,98,184,0.48);
    color: #19294b;
  }}

  /* Lista com scrollbar fina e transparente */
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 6px;
  }}
  #list::-webkit-scrollbar {{
    width: 7px;
  }}
  #list::-webkit-scrollbar-track {{
    background: transparent;
  }}
  #list::-webkit-scrollbar-thumb {{
    background-color: rgba(70, 98, 184, 0.3);
    border-radius: 5px;
  }}
  #list div {{
    padding: 8px 14px;
    margin-bottom: 6px;
    border-radius: 14px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: #374b75;
    background: rgba(255 255 255 / 0.18);
    transition:
      background-color 0.35s ease,
      color 0.35s ease,
      box-shadow 0.25s ease;
    box-shadow: inset 0 0 10px rgba(255 255 255 / 0.1);
    user-select: none;
  }}
  #list div:hover {{
    background-color: rgba(70, 98, 184, 0.22);
    color: #1a2d5a;
    box-shadow:
      0 2px 10px rgba(70, 98, 184, 0.45),
      inset 0 0 15px rgba(255 255 255 / 0.2);
  }}
  #list div.active {{
    background-color: #4662b8;
    color: #e3e7f8;
    box-shadow:
      0 3px 16px #354a96,
      inset 0 0 20px #6384f9;
  }}

  /* Mapa ocupa o restante do espaço */
  #map {{
    flex-grow: 1;
    position: relative;
    overflow: hidden;
    background: linear-gradient(180deg, #dae1f2 0%, #c4cde3 100%);
    box-shadow:
      inset 0 0 40px rgba(255 255 255 / 0.4),
      inset 0 0 20px rgba(0 0 0 / 0.05);
    border-radius: 20px;
    margin: 16px;
  }}
  svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}

  /* Polígonos com cores suaves e hover elegante */
  .area {{
    fill: #9bb4d6;
    stroke: #3a4f7d;
    stroke-width: 1.2;
    cursor: pointer;
    transition: fill 0.35s ease, stroke-width 0.35s ease;
    filter: drop-shadow(0 0 1.5px rgba(30,40,80,0.3));
  }}
  .area:hover {{
    fill: #617bb9;
    stroke-width: 2.2;
    filter: drop-shadow(0 0 5px rgba(70,98,184,0.7));
  }}
  .area.selected {{
    fill: #3b4a87;
    stroke: #1e2a54;
    stroke-width: 2.5;
    filter: drop-shadow(0 0 7px rgba(30,45,90,0.8));
  }}

  /* Tooltip translúcido e sofisticado */
  #tooltip {{
    position: fixed;
    padding: 7px 14px;
    background: rgba(55, 70, 110, 0.85);
    color: #e0e7ff;
    font-size: 14px;
    border-radius: 18px;
    pointer-events: none;
    display: none;
    box-shadow:
      0 0 12px rgba(50, 70, 120, 0.9);
    user-select: none;
    z-index: 1100;
    font-weight: 600;
    letter-spacing: 0.03em;
  }}

  /* Painel de informações transparente, clean e elegante */
  #info {{
    position: fixed;
    right: 28px;
    top: 38px;
    background: rgba(255 255 255 / 0.15);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-radius: 20px;
    border: 1.2px solid rgba(255 255 255 / 0.3);
    box-shadow:
      0 8px 25px rgba(20, 30, 60, 0.18),
      inset 0 0 50px rgba(255 255 255 / 0.35);
    max-width: 340px;
    font-size: 14px;
    line-height: 1.45;
    color: #1b2c55;
    padding: 18px 24px 24px 24px;
    user-select: none;
    display: none;
    z-index: 1200;
    font-weight: 600;
  }}
  #info.visible {{
    display: block;
  }}
  #info h3 {{
    margin: 0 0 14px 0;
    font-size: 22px;
    font-weight: 700;
    color: #1e2f54;
    border-bottom: 1.5px solid rgba(70, 98, 184, 0.4);
    padding-bottom: 8px;
    letter-spacing: 0.05em;
  }}
  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    row-gap: 10px;
    column-gap: 22px;
  }}
  #info .label {{
    font-weight: 600;
    color: #3e5481;
    white-space: nowrap;
    letter-spacing: 0.02em;
  }}
  #info .value {{
    font-weight: 500;
    text-align: right;
    color: #25355a;
    white-space: nowrap;
    overflow-wrap: normal;
    font-variant-numeric: tabular-nums;
  }}
  #info .fonte {{
    grid-column: 1 / -1;
    font-size: 11px;
    color: #7b8bb8;
    font-style: italic;
    margin-top: 18px;
    text-align: right;
  }}

  /* Scrollbar da página (sidebar) mais suave */
  ::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
  }}
  ::-webkit-scrollbar-track {{
    background: transparent;
  }}
  ::-webkit-scrollbar-thumb {{
    background-color: rgba(70, 98, 184, 0.28);
    border-radius: 8px;
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
