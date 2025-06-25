import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configurações da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    page_icon="📍"
)

# CSS customizado minimalista
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1.5rem;
    }
    #map-container {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Título e introdução
st.title("RMC Data")
st.markdown("""
Explore os municípios da Região Metropolitana de Campinas. 
Clique em qualquer município no mapa ou na lista para ver detalhes.
""")

# Carregamento dos dados
@st.cache_data
def load_data():
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
    
    return {"type": "FeatureCollection", "features": features}, df

geojson, df = load_data()
geojson_str = json.dumps(geojson)

# HTML do mapa interativo
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Mapa Interativo RMC</title>
<style>
  html, body {{
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
  }}
  #container {{
    display: flex;
    height: 600px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }}
  #sidebar {{
    width: 250px;
    background: white;
    padding: 15px;
    overflow-y: auto;
    border-right: 1px solid #e1e4e8;
  }}
  #sidebar h2 {{
    margin: 0 0 10px 0;
    font-size: 18px;
    color: #1a2d5a;
  }}
  #search {{
    width: 100%;
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }}
  .municipio-item {{
    padding: 8px;
    margin-bottom: 5px;
    cursor: pointer;
    border-radius: 4px;
    transition: background 0.2s;
  }}
  .municipio-item:hover {{
    background: #f0f3f8;
  }}
  .municipio-item.active {{
    background: #4d648d;
    color: white;
  }}
  #map {{
    flex: 1;
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
    transition: all 0.2s;
  }}
  .area:hover {{
    fill: #8db3dd;
  }}
  .area.selected {{
    fill: #4d648d;
    stroke: #1a2d5a;
  }}
  #info-panel {{
    position: absolute;
    bottom: 20px;
    right: 20px;
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    max-width: 300px;
    display: none;
  }}
  #info-panel h3 {{
    margin-top: 0;
    color: #1a2d5a;
    border-bottom: 1px solid #eee;
    padding-bottom: 8px;
  }}
  .info-row {{
    margin-bottom: 8px;
  }}
  .info-label {{
    font-weight: 600;
    color: #4d648d;
  }}
</style>
</head>
<body>
<div id="container">
  <div id="sidebar">
    <h2>Municípios</h2>
    <input id="search" type="text" placeholder="Buscar município..." />
    <div id="municipios-list"></div>
  </div>
  <div id="map">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
    <div id="info-panel">
      <h3 id="municipio-name">Município</h3>
      <div class="info-row">
        <span class="info-label">PIB 2021:</span>
        <span id="pib-value">-</span>
      </div>
      <div class="info-row">
        <span class="info-label">População:</span>
        <span id="pop-value">-</span>
      </div>
      <div class="info-row">
        <span class="info-label">PIB per capita:</span>
        <span id="percapita-value">-</span>
      </div>
    </div>
  </div>
</div>
<script>
const geo = {geojson_str};
const svg = document.querySelector("svg");
const municipiosList = document.getElementById("municipios-list");
const searchInput = document.getElementById("search");
const infoPanel = document.getElementById("info-panel");

let selectedMunicipio = null;
const paths = {{}};

// Projeção das coordenadas
function project([lon, lat]) {{
  const minX = -47.8, maxX = -46.2;
  const minY = -23.2, maxY = -22.5;
  const x = ((lon - minX) / (maxX - minX)) * 920 + 40;
  const y = 900 - ((lat - minY) / (maxY - minY)) * 880;
  return [x, y];
}}

function polygonToPath(coords) {{
  return coords.map(c => project(c).join(",")).join(" ");
}}

// Selecionar município
function selectMunicipio(name) {{
  if (selectedMunicipio) {{
    paths[selectedMunicipio].classList.remove("selected");
    document.querySelector(`.municipio-item[data-name="${{selectedMunicipio}}"]`).classList.remove("active");
  }}
  
  selectedMunicipio = name;
  paths[name].classList.add("selected");
  document.querySelector(`.municipio-item[data-name="${{name}}"]`).classList.add("active");
  
  // Atualizar painel de informações
  const feature = geo.features.find(f => f.properties.name === name);
  if (feature) {{
    const props = feature.properties;
    document.getElementById("municipio-name").textContent = name;
    document.getElementById("pib-value").textContent = props.pib_2021 ? "R$ " + props.pib_2021.toLocaleString("pt-BR") : "-";
    document.getElementById("pop-value").textContent = props.populacao_2022 ? props.populacao_2022.toLocaleString("pt-BR") : "-";
    document.getElementById("percapita-value").textContent = props.per_capita_2021 ? "R$ " + props.per_capita_2021.toLocaleString("pt-BR") : "-";
    infoPanel.style.display = "block";
  }}
}}

// Criar elementos SVG e lista
geo.features.forEach(f => {{
  const name = f.properties.name;
  
  // Criar caminho SVG
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
  path.addEventListener("click", () => selectMunicipio(name));
  svg.appendChild(path);
  paths[name] = path;
  
  // Criar item da lista
  const item = document.createElement("div");
  item.className = "municipio-item";
  item.textContent = name;
  item.setAttribute("data-name", name);
  item.addEventListener("click", () => selectMunicipio(name));
  municipiosList.appendChild(item);
}});

// Filtro de busca
searchInput.addEventListener("input", () => {{
  const searchTerm = searchInput.value.toLowerCase();
  const items = document.querySelectorAll(".municipio-item");
  
  items.forEach(item => {{
    if (item.textContent.toLowerCase().includes(searchTerm)) {{
      item.style.display = "block";
    }} else {{
      item.style.display = "none";
    }}
  }});
}});

// Selecionar primeiro município por padrão
if (geo.features.length > 0) {{
  selectMunicipio(geo.features[0].properties.name);
}}
</script>
</body>
</html>
"""

# Exibição do mapa
st.markdown('<div id="map-container">', unsafe_allow_html=True)
st.components.v1.html(html_code, height=650)
st.markdown('</div>', unsafe_allow_html=True)

# Seção de informações adicionais
st.markdown("---")
with st.expander("ℹ️ Sobre os dados"):
    st.markdown("""
    - **Fonte dos dados**: IBGE Cidades e outras fontes oficiais
    - **Atualização**: Dados referentes a 2021-2022
    - **Projeção**: Coordenadas geográficas (WGS84)
    """)
