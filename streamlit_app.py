import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Dados
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
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
<title>Mapa Interativo RMC - UltraFino</title>

<!-- Fonte refinada: Inter -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet">

<style>
  /* Reset básico e base */
  *, *::before, *::after {{
    box-sizing: border-box;
  }}
  html, body {{
    margin: 0; padding: 0;
    height: 100vh;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    background: #fefefe;
    color: #3a4058;
    font-weight: 300;
    font-size: 14px;
    line-height: 1.42;
    overflow: hidden;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: flex;
    user-select: none;
  }}

  /* Sidebar - estrutura assimétrica, leve */
  #sidebar {{
    flex: 0 0 250px;
    background: linear-gradient(135deg, #ffffffee 0%, #f9fafcee 100%);
    border-right: 1px solid #e5e8f0;
    box-shadow: inset 3px 0 6px rgba(60, 70, 90, 0.06);
    display: flex;
    flex-direction: column;
    padding: 22px 20px 12px 24px;
    gap: 14px;
  }}

  /* Título sidebar, delicado, com tracking */
  #sidebar h2 {{
    font-weight: 500;
    font-size: 16px;
    letter-spacing: 0.18em;
    color: #667088;
    margin: 0 0 6px 2px;
    user-select: text;
  }}

  /* Input busca minimalista */
  #search {{
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 300;
    color: #5a6278;
    background: #fafbfd;
    border: 1.5px solid #c8d0e7;
    border-radius: 12px;
    outline-offset: 2px;
    outline-color: transparent;
    transition: outline-color 0.2s ease, border-color 0.3s ease;
    user-select: text;
  }}
  #search::placeholder {{
    color: #abb2c2;
    font-style: italic;
  }}
  #search:focus {{
    border-color: #6c7bd1;
    outline-color: #a7b1e3;
    background: #fff;
  }}

  /* Lista de municípios com espaçamento e scroll suavizado */
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 8px;
    scrollbar-width: thin;
    scrollbar-color: #a0a8b3 transparent;
  }}
  #list::-webkit-scrollbar {{
    width: 6px;
  }}
  #list::-webkit-scrollbar-track {{
    background: transparent;
  }}
  #list::-webkit-scrollbar-thumb {{
    background: #a0a8b3;
    border-radius: 5px;
  }}
  #list div {{
    font-weight: 300;
    font-size: 13px;
    line-height: 1.4;
    color: #5b6077;
    padding: 8px 14px;
    border-radius: 16px;
    margin-bottom: 10px;
    cursor: pointer;
    user-select: none;
    border: 1px solid transparent;
    transition:
      color 0.22s ease,
      background-color 0.22s ease,
      box-shadow 0.3s ease,
      border-color 0.22s ease;
  }}
  #list div:hover {{
    background-color: #f3f5fa;
    color: #404f7a;
    border-color: #8a94c1;
    box-shadow: inset 4px 0 8px rgba(138, 148, 193, 0.25);
  }}
  #list div.active {{
    background-color: #6671f0;
    color: #fff;
    font-weight: 400;
    box-shadow: 0 0 14px rgba(102, 113, 240, 0.9);
    border-color: #565fbe;
  }}

  /* Mapa flexível, espaçoso, com padding para área */
  #map {{
    flex-grow: 1;
    background: #ffffff;
    border-radius: 20px 0 0 20px;
    box-shadow: 0 10px 32px rgba(70, 80, 110, 0.12);
    padding: 32px 48px 48px 48px;
    position: relative;
    display: flex;
    flex-direction: column;
  }}

  /* SVG mapa responsivo */
  svg {{
    width: 100%;
    height: 100%;
    display: block;
    border-radius: 12px;
  }}

  /* Polígonos estilo refinado */
  .area {{
    fill: #dde1f7;
    stroke: #6977b8;
    stroke-width: 1;
    cursor: pointer;
    transition: fill 0.33s cubic-bezier(0.4, 0, 0.2, 1),
                stroke-width 0.3s ease,
                filter 0.3s ease;
    filter: drop-shadow(0 0 0 transparent);
  }}
  .area:hover {{
    fill: #6671f0;
    stroke-width: 2;
    filter: drop-shadow(0 0 10px rgba(102, 113, 240, 0.4));
  }}
  .area.selected {{
    fill: #505fb7;
    stroke: #404d99;
    stroke-width: 2.5;
    filter: drop-shadow(0 0 15px rgba(80, 95, 183, 0.7));
  }}

  /* Tooltip minimalista */
  #tooltip {{
    position: fixed;
    background: rgba(80, 95, 183, 0.9);
    color: white;
    font-weight: 400;
    font-size: 12px;
    padding: 6px 12px;
    border-radius: 14px;
    pointer-events: none;
    user-select: none;
    box-shadow: 0 0 12px rgba(80, 95, 183, 0.5);
    display: none;
    z-index: 9000;
    transition: opacity 0.3s ease;
  }}

  /* Caixa flutuante info com blur e leve transparência */
  #info {{
    position: fixed;
    top: 40px;
    right: 36px;
    max-width: 300px;
    background: rgba(255, 255, 255, 0.88);
    border-radius: 24px;
    box-shadow:
      0 16px 28px rgba(102, 113, 240, 0.16),
      0 6px 12px rgba(102, 113, 240, 0.12);
    backdrop-filter: saturate(180%) blur(18px);
    -webkit-backdrop-filter: saturate(180%) blur(18px);
    padding: 24px 28px;
    color: #2f3558;
    font-weight: 300;
    font-size: 14px;
    line-height: 1.45;
    user-select: text;
    display: none;
    border: 1px solid #bec6e3;
    transition: opacity 0.33s ease;
    z-index: 10000;
  }}
  #info.visible {{
    display: block;
    opacity: 1;
  }}
  #info h3 {{
    margin: 0 0 20px 0;
    font-weight: 500;
    font-size: 20px;
    letter-spacing: 0.04em;
    color: #4b5278;
    user-select: text;
  }}

  /* Grid info fina e espaçada */
  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px 26px;
  }}
  #info .label {{
    font-weight: 400;
    color: #7882ad;
    white-space: nowrap;
    user-select: text;
  }}
  #info .value {{
    font-weight: 500;
    color: #4b5278;
    text-align: right;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    user-select: text;
  }}
  #info .fonte {{
    grid-column: 1 / -1;
    font-style: italic;
    font-weight: 300;
    font-size: 12px;
    color: #a6aecf;
    margin-top: 26px;
    text-align: right;
    user-select: none;
  }}

</style>
</head>
<body>
  <aside id="sidebar" role="complementary" aria-label="Lista de municípios">
    <h2>Municípios</h2>
    <input id="search" type="search" placeholder="Buscar município..." aria-label="Buscar município" autocomplete="off" />
    <div id="list" tabindex="0" role="listbox" aria-multiselectable="false" aria-label="Lista de municípios"></div>
  </aside>

  <main id="map" role="main" aria-label="Mapa interativo da Região Metropolitana de Campinas">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" aria-hidden="true"></svg>
    <div id="tooltip" role="tooltip" aria-hidden="true"></div>
  </main>

  <section id="info" role="region" aria-live="polite" aria-label="Informações do município selecionado">
    <h3>Município</h3>
    <div class="grid">
      <div class="label">PIB 2021:</div><div class="value" id="pib"></div>
      <div class="label">% no PIB regional:</div><div class="value" id="part"></div>
      <div class="label">PIB per capita (2021):</div><div class="value" id="percapita"></div>
      <div class="label">População (2022):</div><div class="value" id="pop"></div>
      <div class="label">Área:</div><div class="value" id="area"></div>
      <div class="label">Densidade demográfica:</div><div class="value" id="dens"></div>
      <div class="fonte">Fonte: IBGE Cidades</div>
    </div>
  </section>

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
    const offsetX = 10;
    const offsetY = -28;
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
