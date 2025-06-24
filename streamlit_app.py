import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregamento dos dados geográficos
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

# Carregamento dos dados tabulares
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

# HTML + CSS + JS
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
<title>Mapa Interativo RMC - Profissional</title>

<!-- Fonte refinada -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet" />

<style>
  /* Reset e base */
  *, *::before, *::after {{
    box-sizing: border-box;
  }}
  html, body {{
    margin: 0; padding: 0;
    height: 100vh;
    width: 100vw;
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background: #fafbfc;
    color: #374151;
    font-weight: 300;
    font-size: 14px;
    line-height: 1.5;
    display: flex;
    user-select: none;
    overflow: hidden;
  }}

  /* Sidebar */
  #sidebar {{
    flex: 0 0 260px;
    background: #ffffff;
    border-right: 1px solid #e0e0e0;
    padding: 28px 26px 24px 28px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }}

  #sidebar h2 {{
    font-weight: 500;
    font-size: 16px;
    letter-spacing: 0.16em;
    color: #6b7280;
    margin: 0 0 10px 2px;
    user-select: text;
    text-transform: uppercase;
  }}

  /* Busca */
  #search {{
    padding: 10px 14px;
    font-size: 14px;
    font-weight: 300;
    color: #4b5563;
    border: 1.5px solid #d1d5db;
    border-radius: 12px;
    outline-offset: 2px;
    outline-color: transparent;
    transition: border-color 0.25s ease;
  }}
  #search::placeholder {{
    color: #9ca3af;
    font-style: italic;
  }}
  #search:focus {{
    border-color: #2563eb;
    outline-color: #bfdbfe;
    background-color: #ffffff;
  }}

  /* Lista municípios */
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 8px;
    scrollbar-width: thin;
    scrollbar-color: #cbd5e1 transparent;
  }}
  #list::-webkit-scrollbar {{
    width: 6px;
  }}
  #list::-webkit-scrollbar-track {{
    background: transparent;
  }}
  #list::-webkit-scrollbar-thumb {{
    background-color: #cbd5e1;
    border-radius: 10px;
  }}

  #list div {{
    font-weight: 300;
    font-size: 14px;
    line-height: 1.3;
    color: #374151;
    padding: 10px 16px;
    margin-bottom: 10px;
    border-radius: 14px;
    cursor: pointer;
    user-select: none;
    border: 1.5px solid transparent;
    transition: background-color 0.2s ease, border-color 0.2s ease;
  }}
  #list div:hover {{
    background-color: #eff6ff;
    border-color: #2563eb;
  }}
  #list div.active {{
    background-color: #2563eb;
    color: #fff;
    font-weight: 500;
    border-color: #1e40af;
  }}

  /* Mapa container */
  #map {{
    flex-grow: 1;
    background: #fff;
    border-radius: 0 20px 20px 0;
    padding: 44px 52px;
    box-shadow: 0 4px 12px rgb(55 65 81 / 0.07);
    position: relative;
    display: flex;
    flex-direction: column;
  }}

  svg {{
    width: 100%;
    height: 100%;
    border-radius: 12px;
  }}

  /* Polígonos */
  .area {{
    fill: #cbd5e1;
    stroke: #64748b;
    stroke-width: 1.2;
    cursor: pointer;
    transition: fill 0.3s ease, stroke-width 0.3s ease;
  }}
  .area:hover {{
    fill: #3b82f6;
    stroke-width: 2.2;
  }}
  .area.selected {{
    fill: #2563eb;
    stroke: #1e40af;
    stroke-width: 2.5;
  }}

  /* Tooltip */
  #tooltip {{
    position: fixed;
    pointer-events: none;
    background: #2563eb;
    color: white;
    padding: 5px 14px;
    font-size: 12px;
    border-radius: 10px;
    font-weight: 400;
    user-select: none;
    display: none;
    z-index: 1000;
    white-space: nowrap;
    box-shadow: 0 2px 10px rgb(37 99 235 / 0.5);
  }}

  /* Caixa flutuante info */
  #info {{
    position: fixed;
    top: 40px;
    right: 40px;
    max-width: 310px;
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0 12px 24px rgb(99 102 241 / 0.12);
    padding: 26px 30px;
    font-weight: 300;
    font-size: 14px;
    line-height: 1.5;
    color: #374151;
    user-select: text;
    display: none;
    border: 1.5px solid #e5e7eb;
  }}
  #info.visible {{
    display: block;
  }}

  #info h3 {{
    margin: 0 0 20px 0;
    font-weight: 500;
    font-size: 20px;
    letter-spacing: 0.02em;
    color: #1e293b;
    user-select: text;
  }}

  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px 32px;
  }}

  #info .label {{
    font-weight: 400;
    color: #6b7280;
    white-space: nowrap;
    user-select: text;
  }}

  #info .value {{
    font-weight: 500;
    color: #1e293b;
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
    color: #9ca3af;
    margin-top: 32px;
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
