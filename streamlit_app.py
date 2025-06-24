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
  html, body {{
    height: 100vh;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    background-color: #f9fafa;
    display: flex;
    flex-direction: column;
    overflow: hidden; /* Evita scroll da página */
  }}
  /* Barra horizontal topo */
  #topbar {{
    height: 48px;
    background: #fff;
    border-bottom: 1px solid #e1e4e8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    overflow-x: auto;
    padding: 0 10px;
    user-select: none;
  }}
  #topbar::-webkit-scrollbar {{
    height: 6px;
  }}
  #topbar::-webkit-scrollbar-thumb {{
    background-color: #4d648d;
    border-radius: 3px;
  }}
  #topbar div {{
    white-space: nowrap;
    padding: 8px 14px;
    margin: 0 6px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
    color: #1a2d5a;
    transition: background-color 0.3s, color 0.3s;
  }}
  #topbar div:hover {{
    background-color: #e3ecf9;
  }}
  #topbar div.active {{
    background-color: #4d648d;
    color: white;
    font-weight: 600;
  }}

  /* Área principal - mapa e painel info */
  #main {{
    flex-grow: 1;
    display: flex;
    position: relative;
    overflow: hidden;
  }}
  #map {{
    flex-grow: 1;
    position: relative;
    overflow: hidden; /* Impede scroll no mapa */
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
    position: fixed; /* fixado na tela */
    padding: 5px 10px;
    background: rgba(30, 60, 120, 0.95);
    color: white;
    font-size: 13px;
    border-radius: 5px;
    pointer-events: none;
    display: none;
    box-shadow: 0 0 8px rgba(0,0,0,0.1);
    z-index: 1000;
    user-select: none;
  }}

  /* Painel de Informações */
  #info {{
    width: 320px;
    background: #f0f3f8;
    padding: 16px 20px;
    border-radius: 10px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.1);
    font-size: 14px;
    line-height: 1.4;
    color: #1a2d5a;
    user-select: none;
    border: 1px solid #d9e2f3;
    z-index: 20;
    overflow-y: auto;
  }}
  #info.hidden {{
    display: none;
  }}
  #info h3 {{
    margin: 0 0 12px 0;
    font-size: 20px;
    font-weight: 700;
    color: #2c3e70;
    border-bottom: 1px solid #c3d0e8;
    padding-bottom: 6px;
  }}
  #info .grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    row-gap: 8px;
    column-gap: 24px;
  }}
  #info .label {{
    font-weight: 600;
    color: #4d648d;
    white-space: nowrap;
  }}
  #info .value {{
    font-weight: 500;
    text-align: right;
    color: #34495e;
    overflow-wrap: break-word;
  }}
  #info .fonte {{
    grid-column: 1 / -1;
    font-size: 11px;
    color: #7f8caa;
    font-style: italic;
    margin-top: 16px;
    text-align: right;
  }}

  /* Scrollbar no painel info */
  #info::-webkit-scrollbar {{
    width: 6px;
  }}
  #info::-webkit-scrollbar-thumb {{
    background-color: #4d648d;
    border-radius: 3px;
  }}
</style>
</head>
<body>
  <div id="topbar" role="list" aria-label="Lista de municípios">
    <!-- Itens serão inseridos pelo JS -->
  </div>
  <div id="main">
    <div id="map" role="main" aria-label="Mapa interativo da Região Metropolitana de Campinas">
      <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
      <div id="tooltip" role="tooltip" aria-hidden="true"></div>
    </div>
    <div id="info" class="hidden" role="region" aria-live="polite" aria-label="Informações do município selecionado">
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
  </div>
<script>
const geo = {geojson_str};
const svg = document.querySelector("svg");
const tooltip = document.getElementById("tooltip");
const info = document.getElementById("info");
const topbar = document.getElementById("topbar");

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
    [...topbar.children].forEach(d => d.classList.remove("active"));
  }}
  selected = name;
  if (paths[name]) {{
    paths[name].classList.add("selected");
    [...topbar.children].forEach(div => {{
      if(div.textContent === name) {{
        div.classList.add("active");
        // Scroll horizontal suave para o item ativo na barra horizontal
        const container = topbar;
        const containerWidth = container.clientWidth;
        const containerLeft = container.getBoundingClientRect().left;

        const elementLeft = div.getBoundingClientRect().left;
        const elementWidth = div.offsetWidth;

        const scrollLeft = container.scrollLeft;
        const offset = elementLeft - containerLeft;

        const scrollTo = scrollLeft + offset - containerWidth / 2 + elementWidth / 2;

        container.scrollTo({{ left: scrollTo, behavior: "smooth" }});
      }}
    }});
    showInfo(name);
  }}
}}

function showInfo(name) {{
  const f = geo.features.find(f => f.properties.name === name);
  if (!f) return;
  info.classList.remove("hidden");
  info.querySelector("h3").textContent = name;
  info.querySelector("#pib").textContent = f.properties.pib_2021 ? "R$ " + f.properties.pib_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace('.', ',') + "%" : "-";
  info.querySelector("#percapita").textContent = f.properties.per_capita_2021 ? "R$ " + f.properties.per_capita_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#pop").textContent = f.properties.populacao_2022 ? f.properties.populacao_2022.toLocaleString("pt-BR") : "-";
  info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace(".", ",") + " km²" : "-";
  info.querySelector("#dens").textContent = f.properties.densidade_demografica_2022 ? f.properties.densidade_demografica_2022.toLocaleString("pt-BR") + " hab/km²" : "-";
}}

function createTopbarItems() {{
  geo.features.forEach(f => {{
    const name = f.properties.name;
    const div = document.createElement("div");
    div.textContent = name;
    div.tabIndex = 0;
    div.setAttribute('role', 'option');
    div.addEventListener("click", () => select(name));
    div.addEventListener("keydown", e => {{
      if (e.key === "Enter" || e.key === " ") {{
        e.preventDefault();
        select(name);
      }}
    }});
    topbar.appendChild(div);
  }});
}}

createTopbarItems();

// Seleciona primeiro município ao carregar
if(geo.features.length > 0) {{
  select(geo.features[0].properties.name);
}}
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=700, scrolling=False)
