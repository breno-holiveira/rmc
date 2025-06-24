import streamlit as st
import geopandas as gpd
import pandas as pd
import json

# Configurações da página
st.set_page_config(page_title="Mapa Interativo RMC", layout="wide", initial_sidebar_state="expanded")

st.title("Mapa Interativo da Região Metropolitana de Campinas (RMC)")
st.markdown("Clique no município para ver detalhes. Passe o mouse para ver nome.")

# --- Carregar shapefile ---
shp_path = "./shapefile_rmc/RMC_municipios.shp"  # ajuste seu caminho
gdf = gpd.read_file(shp_path)

# Garantir CRS EPSG:4326 para GeoJSON funcionar bem
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")

gdf = gdf.sort_values("NM_MUN")

# --- Carregar dados ---
# Pode ser Excel (.xlsx) ou CSV; aqui exemplo CSV
dados_path = "./planilhas/dados_rmc.csv"  # ajuste seu caminho
df_dados = pd.read_csv(dados_path)

# Normalizar nome para index (ajuste a coluna que tem o nome dos municípios)
df_dados.set_index("nome", inplace=True)

# --- Construir GeoJSON com propriedades dos dados ---
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    if nome in df_dados.index:
        dados = df_dados.loc[nome]
        props = {
            "name": nome,
            "pib_2021": dados.get("pib_2021", None),
            "participacao_rmc": dados.get("participacao_rmc", None),
            "pib_per_capita": dados.get("pib_per_capita", None),
            "populacao": dados.get("populacao", None),
            "area": dados.get("area", None),
            "densidade_demografica": dados.get("densidade_demografica", None),
        }
    else:
        props = {
            "name": nome,
            "pib_2021": None,
            "participacao_rmc": None,
            "pib_per_capita": None,
            "populacao": None,
            "area": None,
            "densidade_demografica": None,
        }
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson_str = json.dumps({"type": "FeatureCollection", "features": features})

# --- HTML com SVG + JS ---
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC</title>
<style>
  html, body {{
    margin: 0; padding: 0; height: 100vh; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f9f9f9; color: #222; display: grid;
    grid-template-columns: 280px 1fr 350px;
    grid-template-rows: 100vh;
    overflow: hidden;
  }}
  #legend {{
    background: #fff; border-right: 1px solid #ddd; padding: 20px; overflow-y: auto;
    box-shadow: 2px 0 6px rgba(0,0,0,0.05);
  }}
  #legend strong {{
    color: #0b3d91; font-size: 18px; border-bottom: 2px solid #0b3d91; display: block; margin-bottom: 10px; font-weight: 700;
  }}
  #legend div {{
    cursor: pointer; padding: 8px 12px; margin-bottom: 4px; border-radius: 6px; transition: background-color 0.3s;
    font-size: 14px; color: #222;
  }}
  #legend div:hover, #legend div.active {{
    background: #0b3d91; color: #fff;
    font-weight: 700;
  }}
  #map-container {{
    position: relative; background: white; overflow: hidden;
  }}
  svg {{
    width: 100%; height: 100vh; display: block;
  }}
  .municipio {{
    fill: rgba(11, 61, 145, 0.15);
    stroke: rgba(11, 61, 145, 0.6);
    stroke-width: 1;
    cursor: pointer;
    transition: all 0.25s ease;
  }}
  .municipio:hover {{
    fill: rgba(11, 61, 145, 0.4);
    stroke-width: 2;
    filter: drop-shadow(0 0 6px rgba(11, 61, 145, 0.3));
  }}
  .municipio.selected {{
    fill: rgba(11, 61, 145, 0.6);
    stroke: rgba(11, 61, 145, 1);
    stroke-width: 3;
    filter: drop-shadow(0 0 12px rgba(11, 61, 145, 0.6));
  }}
  #tooltip {{
    position: absolute; pointer-events: none;
    background: rgba(11,61,145,0.85);
    color: white; font-size: 13px; font-weight: 600;
    padding: 6px 12px; border-radius: 6px;
    display: none;
    white-space: nowrap;
    z-index: 1000;
  }}
  #info-panel {{
    background: #fff; border-left: 1px solid #ddd;
    padding: 24px; font-size: 15px;
    overflow-y: auto;
    display: flex; flex-direction: column;
  }}
  #info-panel h2 {{
    margin-top: 0; color: #0b3d91;
    border-bottom: 2px solid #0b3d91;
    padding-bottom: 8px;
  }}
  #info-panel .field {{
    margin-bottom: 14px;
  }}
  #info-panel .field strong {{
    color: #0b3d91;
  }}
  #info-panel .field span {{
    margin-left: 6px;
    color: #222;
  }}
  #info-panel #close-btn {{
    align-self: flex-end;
    background: none; border: none;
    font-size: 22px;
    color: #0b3d91;
    cursor: pointer;
    margin-bottom: 12px;
  }}
  #info-panel .fonte {{
    font-size: 12px; color: #666; margin-top: auto; font-style: italic; text-align: right;
  }}
</style>
</head>
<body>

<nav id="legend" aria-label="Lista de municípios">
  <strong>Municípios da RMC</strong>
  <div id="municipios-list"></div>
</nav>

<div id="map-container" role="main" aria-label="Mapa dos municípios">
  <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg"></svg>
  <div id="tooltip"></div>
</div>

<aside id="info-panel" aria-label="Informações do município" hidden>
  <button id="close-btn" aria-label="Fechar painel">&times;</button>
  <h2 id="info-name">Selecione um município</h2>
  <div class="field"><strong>PIB (2021):</strong> <span id="info-pib">-</span></div>
  <div class="field"><strong>Participação na RMC:</strong> <span id="info-participacao">-</span></div>
  <div class="field"><strong>PIB per capita (2021):</strong> <span id="info-percapita">-</span></div>
  <div class="field"><strong>População:</strong> <span id="info-populacao">-</span></div>
  <div class="field"><strong>Área (km²):</strong> <span id="info-area">-</span></div>
  <div class="field"><strong>Densidade demográfica (2022):</strong> <span id="info-densidade">-</span></div>
  <div class="fonte">Fonte: IBGE Cidades</div>
</aside>

<script>
  const geojson = {geojson_str};

  const svg = document.querySelector("svg");
  const tooltip = document.getElementById("tooltip");
  const infoPanel = document.getElementById("info-panel");
  const closeBtn = document.getElementById("close-btn");

  // Projeção simples para coordenadas geo para SVG (proj linear)
  // Ajustar para encaixar bem no viewBox 1000x950
  const margin = 20;
  let bounds = [Infinity, Infinity, -Infinity, -Infinity]; // xmin, ymin, xmax, ymax
  geojson.features.forEach(f => {{
    f.geometry.coordinates.flat(Infinity).forEach(coord => {{
      if (coord[0] < bounds[0]) bounds[0] = coord[0];
      if (coord[1] < bounds[1]) bounds[1] = coord[1];
      if (coord[0] > bounds[2]) bounds[2] = coord[0];
      if (coord[1] > bounds[3]) bounds[3] = coord[1];
    }});
  }});

  const width = 1000 - margin*2;
  const height = 950 - margin*2;
  const scaleX = width / (bounds[2] - bounds[0]);
  const scaleY = height / (bounds[3] - bounds[1]);

  function proj(x, y) {{
    return [
      margin + (x - bounds[0]) * scaleX,
      margin + height - (y - bounds[1]) * scaleY // inverter Y para SVG
    ];
  }}

  // Criar path SVG para polígonos
  function polygonPath(coords) {{
    let path = "";
    coords.forEach(ring => {{
      path += "M";
      ring.forEach((point, i) => {{
        const [x,y] = proj(point[0], point[1]);
        path += (i === 0 ? "" : "L") + x.toFixed(2) + "," + y.toFixed(2);
      }});
      path += "Z ";
    }});
    return path.trim();
  }}

  // Desenhar polígonos
  geojson.features.forEach((feature, i) => {{
    const pathData = polygonPath(feature.geometry.coordinates);
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathData);
    path.classList.add("municipio");
    path.dataset.index = i;
    svg.appendChild(path);
  }});

  const municipiosList = document.getElementById("municipios-list");

  // Criar lista lateral
  geojson.features.forEach((feature, i) => {{
    const div = document.createElement("div");
    div.textContent = feature.properties.name;
    div.dataset.index = i;
    municipiosList.appendChild(div);
  }});

  let selectedIndex = null;

  // Função para formatar números grandes
  function fmtNum(n) {{
    if (n === null || n === undefined) return "-";
    if (typeof n === "number") {{
      return n.toLocaleString("pt-BR");
    }}
    return n;
  }}

  // Evento mouseover para tooltip e highlight
  function onMouseOver(e) {{
    const idx = e.target.dataset.index;
    if (idx === undefined) return;
    const feature = geojson.features[idx];
    tooltip.style.display = "block";
    tooltip.textContent = feature.properties.name;
  }}

  // Evento mousemove para posicionar tooltip
  function onMouseMove(e) {{
    tooltip.style.left = (e.pageX + 15) + "px";
    tooltip.style.top = (e.pageY + 15) + "px";
  }}

  // Evento mouseout para esconder tooltip
  function onMouseOut(e) {{
    tooltip.style.display = "none";
  }}

  // Atualiza painel info
  function showInfo(idx) {{
    const f = geojson.features[idx];
    selectedIndex = idx;

    // Remove selected de todos
    document.querySelectorAll(".municipio").forEach(p => p.classList.remove("selected"));
    document.querySelectorAll("#municipios-list > div").forEach(d => d.classList.remove("active"));

    // Seleciona o clicado
    svg.querySelector(`path[data-index='${{idx}}']`).classList.add("selected");
    municipiosList.querySelector(`div[data-index='${{idx}}']`).classList.add("active");

    infoPanel.hidden = false;
    document.getElementById("info-name").textContent = f.properties.name;
    document.getElementById("info-pib").textContent = fmtNum(f.properties.pib_2021);
    document.getElementById("info-participacao").textContent = fmtNum(f.properties.participacao_rmc);
    document.getElementById("info-percapita").textContent = fmtNum(f.properties.pib_per_capita);
    document.getElementById("info-populacao").textContent = fmtNum(f.properties.populacao);
    document.getElementById("info-area").textContent = fmtNum(f.properties.area);
    document.getElementById("info-densidade").textContent = fmtNum(f.properties.densidade_demografica);
  }}

  // Clique nos polígonos
  svg.querySelectorAll(".municipio").forEach(path => {{
    path.addEventListener("mouseover", onMouseOver);
    path.addEventListener("mousemove", onMouseMove);
    path.addEventListener("mouseout", onMouseOut);
    path.addEventListener("click", e => {{
      showInfo(e.target.dataset.index);
    }});
  }});

  // Clique na lista lateral
  municipiosList.querySelectorAll("div").forEach(div => {{
    div.addEventListener("click", e => {{
      showInfo(e.target.dataset.index);
    }});
  }});

  // Fechar painel info
  closeBtn.addEventListener("click", () => {{
    infoPanel.hidden = true;
    selectedIndex = null;
    document.querySelectorAll(".municipio").forEach(p => p.classList.remove("selected"));
    document.querySelectorAll("#municipios-list > div").forEach(d => d.classList.remove("active"));
  }});
</script>

</body>
</html>
"""

# Exibe no Streamlit com altura suficiente
st.components.v1.html(html_code, height=750, scrolling=True)
