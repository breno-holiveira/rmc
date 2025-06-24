import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configurações da página
st.set_page_config(page_title="RMC Data", layout="wide")

st.title("📍 Mapa Interativo da RMC")
st.markdown("**Explore os municípios da Região Metropolitana de Campinas com dados confiáveis.**")

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
  html, body {{
    height: 100vh;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f9fafa;
    display: flex;
    overflow: hidden;
  }}
  /* Sidebar com busca e lista */
  #sidebar {{
    width: 260px;
    background: #fff;
    padding: 20px 16px 12px 16px;
    border-right: 1px solid #e1e4e8;
    box-shadow: 1px 0 5px rgba(0,0,0,0.03);
    display: flex;
    flex-direction: column;
  }}
  #sidebar h2 {{
    margin: 0 0 8px 0;
    font-size: 18px;
    font-weight: 600;
    color: #1a2d5a;
    user-select: none;
  }}
  #search {{
    margin-bottom: 12px;
    padding: 8px 12px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 8px;
    outline-offset: 2px;
    transition: border-color 0.3s;
  }}
  #search:focus {{
    border-color: #4d648d;
    box-shadow: 0 0 5px rgba(77, 100, 141, 0.5);
  }}
  #list {{
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 6px;
  }}
  #list div {{
    padding: 8px 12px;
    margin-bottom: 6px;
    border-radius: 8px;
    cursor: pointer;
    user-select: none;
    font-size: 15px;
    color: #1a2d5a;
    transition: background-color 0.3s, color 0.3s;
  }}
  #list div:hover {{
    background-color: #e3ecf9;
  }}
  #list div.active {{
    background-color: #4d648d;
    color: #fff;
    font-weight: 600;
  }}

  /* Mapa e SVG */
  #map {{
    flex-grow: 1;
    position: relative;
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
    position: absolute;
    padding: 5px 10px;
    background: rgba(30, 60, 120, 0.95);
    color: white;
    font-size: 13px;
    border-radius: 5px;
    pointer-events: none;
    display: none;
    box-shadow: 0 0 8px rgba(0,0,0,0.1);
    z-index: 10;
  }}

  /* Info Box refinado e intuitivo */
  #info {{
    position: fixed;
    right: 30px;
    top: 40px;
    background: #fff;
    padding: 24px 28px;
    border-radius: 14px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.1);
    max-width: 340px;
    font-size: 15px;
    line-height: 1.6;
    display: none;
    border: 1px solid #d8dee9;
    z-index: 20;
    color: #1a2d5a;
    user-select: none;
  }}
  #info.visible {{
    display: block;
  }}
  #info h3 {{
    margin-top: 0;
    font-size: 22px;
    font-weight: 700;
    border-bottom: 2px solid #4d648d;
    padding-bottom: 10px;
    color: #223763;
  }}
  #info .data-row {{
    display: flex;
    justify-content: space-between;
    margin: 10px 0;
  }}
  #info .label {{
    font-weight: 600;
    color: #4d648d;
  }}
  #info .value {{
    font-weight: 500;
    color: #334a80;
  }}
  #info .fonte {{
    font-size: 12px;
    margin-top: 20px;
    color: #777;
    font-style: italic;
    text-align: right;
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
    <div class="data-row"><div class="label">PIB 2021:</div> <div class="value" id="pib"></div></div>
    <div class="data-row"><div class="label">Participação RMC:</div> <div class="value" id="part"></div></div>
    <div class="data-row"><div class="label">PIB per capita:</div> <div class="value" id="percapita"></div></div>
    <div class="data-row"><div class="label">População:</div> <div class="value" id="pop"></div></div>
    <div class="data-row"><div class="label">Área:</div> <div class="value" id="area"></div></div>
    <div class="data-row"><div class="label">Densidade demográfica:</div> <div class="value" id="dens"></div></div>
    <div class="fonte">Fonte: IBGE Cidades</div>
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

// Coordenadas para projeção simples
let coords = [];
geo.features.forEach(f => {{
  const g = f.geometry;
  if (g.type === "Polygon") g.coordinates[0].forEach(c => coords.push(c));
  else g.geometry.coordinates.forEach(p => p[0].forEach(c => coords.push(c)));
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

function formatValue(value, type) {{
  if (value === undefined || value === null || value === "" || isNaN(value) && type !== "percent") return "-";
  switch(type) {{
    case "currency":
      return "R$ " + Number(value).toLocaleString("pt-BR");
    case "percent":
      return (Number(value) * 100).toFixed(2).replace('.', ',') + "%";
    case "number":
      return Number(value).toLocaleString("pt-BR");
    case "area":
      return Number(value).toFixed(2).replace(".", ",") + " km²";
    case "density":
      return Number(value).toLocaleString("pt-BR") + " hab/km²";
    default:
      return value;
  }}
}}

function select(name) {{
  if (selected) {{
    paths[selected].classList.remove("selected");
    [...list.children].forEach(d => d.classList.remove("active"));
  }}
  selected = name;
  if (paths[name]) {{
    paths[name].classList.add("selected");

    // Barra lateral scroll suave
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

        container.scrollTo({{ top: scrollTo, behavior: 'smooth' }});
      }}
    }});
    showInfo(name);
  }}
}}

function showInfo(name) {{
  const f = geo.features.find(f => f.properties.name === name);
  if (!f) return;
  info.querySelector("h3").textContent = name;
  
  info.querySelector("#pib").textContent = formatValue(f.properties.pib_2021, "currency");
  info.querySelector("#part").textContent = formatValue(f.properties.participacao_rmc, "percent");
  info.querySelector("#percapita").textContent = formatValue(f.properties.pib_per_capita, "currency");
  info.querySelector("#pop").textContent = formatValue(f.properties.populacao, "number");
  info.querySelector("#area").textContent = formatValue(f.properties.area, "area");
  info.querySelector("#dens").textContent = formatValue(f.properties.densidade_demografica, "density");

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

// Cria polígonos e itens da legenda
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

  // Eventos do mapa
  path.addEventListener("mousemove", e => {{
    tooltip.style.left = (e.clientX + 10) + "px";
    tooltip.style.top = (e.clientY + 10) + "px";
    tooltip.style.display = "block";
    tooltip.textContent = name;
  }});
  path.addEventListener("mouseleave", () => {{
    tooltip.style.display = "none";
  }});
  path.addEventListener("click", () => select(name));

  // Item da legenda
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
  // Se só 1 item visível, seleciona automaticamente
  const visibleItems = [...list.children].filter(d => d.style.display !== "none");
  if(visibleItems.length === 1) {{
    select(visibleItems[0].dataset.name);
  }}
}});

// Seleciona o primeiro município ao carregar
if(geo.features.length > 0) {{
  select(geo.features[0].properties.name);
}}
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=650, scrolling=False)
