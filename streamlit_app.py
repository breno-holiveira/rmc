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
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
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
    color: #34495e;
  }}
  /* LEGENDA REFINADA */
  #sidebar {{
    width: 260px;
    background: #ffffff;
    padding: 24px 20px 20px 20px;
    border-right: 1px solid #dfe6eb;
    box-shadow: 2px 0 12px rgba(100, 110, 120, 0.06);
    display: flex;
    flex-direction: column;
    font-size: 16px;
    user-select: none;
  }}
  #sidebar > strong {{
    font-size: 22px;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 20px;
    border-bottom: 3px solid #2980b9;
    padding-bottom: 10px;
  }}
  #search-box {{
    padding: 12px 16px;
    font-size: 16px;
    border: 1.8px solid #b0bec5;
    border-radius: 14px;
    outline-offset: 2px;
    background: #fefefe;
    font-weight: 600;
    color: #34495e;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 20px;
    user-select: text;
    box-shadow: inset 0 1px 3px #e0e7ed;
  }}
  #search-box::placeholder {{
    color: #90a4ae;
    font-weight: 500;
  }}
  #search-box:focus {{
    border-color: #2980b9;
    box-shadow: 0 0 10px #5dade2cc;
  }}
  #list {{
    overflow-y: auto;
    flex-grow: 1;
    scrollbar-width: thin;
    scrollbar-color: #b0bec5 transparent;
  }}
  #list::-webkit-scrollbar {{
    width: 8px;
  }}
  #list::-webkit-scrollbar-thumb {{
    background-color: #b0bec5;
    border-radius: 6px;
  }}
  #list > div {{
    padding: 14px 22px;
    border-radius: 14px;
    margin-bottom: 10px;
    cursor: pointer;
    font-weight: 600;
    color: #34495e;
    transition: background-color 0.35s ease, color 0.35s ease, box-shadow 0.35s ease;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    user-select: none;
  }}
  #list > div:hover {{
    background-color: #d6e6fb;
    color: #1a4f8a;
    box-shadow: 0 3px 8px rgba(41, 128, 185, 0.3);
  }}
  #list > div.active {{
    background-color: #2980b9;
    color: #fff;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(41, 128, 185, 0.45);
  }}

  /* MAPA */
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
  #tooltip {{
    position: absolute;
    padding: 6px 12px;
    background: rgba(30, 60, 120, 0.95);
    color: white;
    font-size: 13px;
    border-radius: 7px;
    pointer-events: none;
    display: none;
    box-shadow: 0 0 8px rgba(0,0,0,0.12);
  }}
  /* PAINEL DE INFORMAÇÕES */
  #info {{
    position: fixed;
    right: 30px;
    top: 40px;
    background: #fff;
    padding: 22px 26px;
    border-radius: 16px;
    box-shadow: 0 6px 30px rgba(0,0,0,0.09);
    max-width: 320px;
    font-size: 15px;
    line-height: 1.6;
    display: none;
    border: 1px solid #d8dee9;
    color: #2c3e50;
  }}
  #info.visible {{
    display: block;
  }}
  #info h3 {{
    margin-top: 0;
    color: #2c3e50;
    font-size: 20px;
    border-bottom: 1.8px solid #ccc;
    padding-bottom: 10px;
    font-weight: 700;
  }}
  #info div {{
    margin: 8px 0;
  }}
  #info .fonte {{
    font-size: 12px;
    margin-top: 14px;
    color: #777;
    font-style: italic;
  }}
</style>
</head>
<body>
  <div id="sidebar" role="complementary" aria-label="Lista de municípios">
    <strong>Municípios</strong>
    <input type="search" id="search-box" placeholder="Buscar município..." autocomplete="off" aria-label="Buscar município" />
    <div id="list" tabindex="0" role="listbox" aria-multiselectable="false" aria-label="Lista de municípios"></div>
  </div>

  <div id="map" role="main" aria-label="Mapa interativo da Região Metropolitana de Campinas">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
    <div id="tooltip" role="tooltip" aria-hidden="true"></div>
  </div>

  <div id="info" role="region" aria-live="polite" aria-label="Informações do município selecionado">
    <h3>Município</h3>
    <div><strong>PIB 2021:</strong> <span id="pib"></span></div>
    <div><strong>Participação RMC:</strong> <span id="part"></span></div>
    <div><strong>PIB per capita:</strong> <span id="percapita"></span></div>
    <div><strong>População:</strong> <span id="pop"></span></div>
    <div><strong>Área:</strong> <span id="area"></span></div>
    <div><strong>Densidade demográfica:</strong> <span id="dens"></span></div>
    <div class="fonte">Fonte: IBGE Cidades</div>
  </div>

<script>
const geo = {geojson_str};
const svg = document.querySelector("svg");
const tooltip = document.getElementById("tooltip");
const info = document.getElementById("info");
const list = document.getElementById("list");
const searchBox = document.getElementById("search-box");

let selected = null;
const paths = {{}};

// Coordenadas para projeção simples
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
    document.querySelector(`#list div[data-name='${{name}}']`).classList.add("active");
    showInfo(name);
  }}
}}

function showInfo(name) {{
  const f = geo.features.find(f => f.properties.name === name);
  if (!f) return;
  info.querySelector("h3").textContent = name;
  info.querySelector("#pib").textContent = f.properties.pib_2021 ? "R$ " + f.properties.pib_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace('.', ',') + "%" : "-";
  info.querySelector("#percapita").textContent = f.properties.pib_per_capita ? "R$ " + f.properties.pib_per_capita.toLocaleString("pt-BR") : "-";
  info.querySelector("#pop").textContent = f.properties.populacao ? f.properties.populacao.toLocaleString("pt-BR") : "-";
  info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace(".", ",") + " km²" : "-";
  info.querySelector("#dens").textContent = f.properties.densidade_demografica ? f.properties.densidade_demografica.toLocaleString("pt-BR") + " hab/km²" : "-";
  info.classList.add("visible");
}}

// Montar polígonos e lista da legenda
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

  // Eventos no mapa
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
  div.setAttribute("role", "option");
  div.addEventListener("click", () => select(name));
  div.addEventListener("keydown", e => {{
    if(e.key === "Enter" || e.key === " ") {{
      e.preventDefault();
      select(name);
    }}
  }});
  list.appendChild(div);
}});

// Busca dinâmica na legenda
searchBox.addEventListener("input", e => {{
  const val = e.target.value.toLowerCase();
  Array.from(list.children).forEach(div => {{
    div.style.display = div.textContent.toLowerCase().includes(val) ? "" : "none";
  }});
}});

// Seleciona o primeiro município automaticamente
if(geo.features.length > 0) {{
  select(geo.features[0].properties.name);
  const firstActive = list.querySelector("div.active");
  if(firstActive) firstActive.scrollIntoView({{behavior: "smooth", block: "center"}});
}}
</script>
</body>
</html>
"""

# Renderiza o HTML no app
st.components.v1.html(html_code, height=720, scrolling=False)
