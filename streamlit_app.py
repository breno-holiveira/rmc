import streamlit as st
import geopandas as gpd
import json
from pathlib import Path

# Configurações da página Streamlit
st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="collapsed")

# Título e descrição
st.title("RMC Data")
st.header("Dados e indicadores da Região Metropolitana de Campinas")

# Dicionário com dados adicionais
dados_extra = {
    "Americana": {"populacao": 240000, "area": 140.5, "pib_2021": 12_500_000_000},
    "Artur Nogueira": {"populacao": 56000, "area": 140.2, "pib_2021": 2_200_000_000},
    "Campinas": {"populacao": 1200000, "area": 796.0, "pib_2021": 105_000_000_000},
    "Cosmópolis": {"populacao": 70000, "area": 154.5, "pib_2021": 3_100_000_000},
    "Engenheiro Coelho": {"populacao": 17000, "area": 130.1, "pib_2021": 900_000_000},
    "Holambra": {"populacao": 13000, "area": 65.7, "pib_2021": 850_000_000},
    "Hortolândia": {"populacao": 240000, "area": 62.5, "pib_2021": 9_500_000_000},
    "Indaiatuba": {"populacao": 260000, "area": 311.4, "pib_2021": 15_000_000_000},
    "Itatiba": {"populacao": 120000, "area": 322.3, "pib_2021": 6_500_000_000},
    "Jaguariúna": {"populacao": 57000, "area": 141.2, "pib_2021": 3_200_000_000},
    "Monte Mor": {"populacao": 46000, "area": 155.1, "pib_2021": 2_700_000_000},
    "Morungaba": {"populacao": 14000, "area": 146.4, "pib_2021": 1_100_000_000},
    "Nova Odessa": {"populacao": 62000, "area": 73.3, "pib_2021": 3_600_000_000},
    "Paulínia": {"populacao": 110000, "area": 131.3, "pib_2021": 18_500_000_000},
    "Santa Bárbara d'Oeste": {"populacao": 210000, "area": 310.4, "pib_2021": 10_500_000_000},
    "Santo Antônio de Posse": {"populacao": 31000, "area": 154.0, "pib_2021": 1_600_000_000},
    "Sumaré": {"populacao": 280000, "area": 153.3, "pib_2021": 14_200_000_000},
    "Valinhos": {"populacao": 125000, "area": 148.0, "pib_2021": 7_400_000_000},
    "Vinhedo": {"populacao": 80000, "area": 148.8, "pib_2021": 5_900_000_000},
}

# Carregando shapefile e projetando para WGS84 (EPSG:4326)
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")

gdf = gdf.sort_values(by="NM_MUN")

# Construindo GeoJSON com dados extras
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    extra = dados_extra.get(nome, {"populacao": None, "area": None, "pib_2021": None})
    features.append({
        "type": "Feature",
        "properties": {
            "name": nome,
            "populacao": extra["populacao"],
            "area": extra["area"],
            "pib_2021": extra["pib_2021"]
        },
        "geometry": geom
    })

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

# HTML/JS para o mapa interativo embutido no Streamlit
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC - Transparência</title>
<style>
  /* Reset básico */
  *, *::before, *::after {{
    box-sizing: border-box;
  }}
  html, body {{
    margin: 0; padding: 0;
    height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    background-color: #transparent;
    color: #222;
    display: flex;
    overflow: hidden;
  }}

  /* Sidebar da legenda */
  #legend {{
    width: 220px;
    background: #fff;
    padding: 16px 20px;
    box-shadow: 2px 0 8px rgba(0,0,0,0.08);
    border-right: 1px solid #e3e6ea;
    overflow-y: auto;
  }}
  #legend strong {{
    display: block;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 12px;
    color: #0b3d91;
  }}
  #legend div {{
    margin-bottom: 8px;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
    color: #3a3a3a;
    font-size: 14px;
  }}
  #legend div:hover {{
    background-color: ;
    color: #08318d;
  }}
  #legend div.active {{
    background-color: #0b3d91;
    color: #fff;
    font-weight: 700;
  }}

  /* Container do mapa */
  #map {{
    flex-grow: 1;
    position: relative;
    background: #fff;
  }}
  svg {{
    width: 100%;
    height: 100vh;
    display: block;
    user-select: none;
  }}

  /* Painel de informação */
  #info-panel {{
    width: 280px;
    background: #fff;
    padding: 20px 24px;
    border-left: 1px solid #e3e6ea;
    box-shadow: -2px 0 8px rgba(0,0,0,0.05);
    color: #333;
    font-size: 15px;
    line-height: 1.5;
    overflow-y: auto;
  }}
  #info-panel h3 {{
    margin-top: 0;
    font-weight: 700;
    font-size: 16px;
    color: #0b3d91;
    border-bottom: 2px solid #0b3d91;
    padding-bottom: 8px;
    margin-bottom: 16px;
  }}
  #info-panel div {{
    margin-bottom: 14px;
  }}
  #info-panel div strong {{
    display: inline-block;
    width: 100px;
    color: #0b3d91;
  }}

  /* Polígonos */
  .polygon {{
    fill: rgba(11, 61, 145, 0.15);
    stroke: rgba(11, 61, 145, 0.6);
    stroke-width: 1;
    cursor: pointer;
    transition: fill 0.25s ease, stroke 0.25s ease;
    opacity: 0.85;
  }}
  .polygon:hover {{
    fill: rgba(11, 61, 145, 0.35);
    stroke-width: 2;
    filter: drop-shadow(0 0 6px rgba(11, 61, 145, 0.3));
  }}
  .polygon.selected {{
    fill: rgba(11, 61, 145, 0.45);
    stroke: rgba(11, 61, 145, 0.8);
    stroke-width: 2.5;
    filter: drop-shadow(0 0 10px rgba(11, 61, 145, 0.5));
  }}

  /* Tooltip */
  #tooltip {{
    position: absolute;
    pointer-events: none;
    padding: 6px 12px;
    background: rgba(11, 61, 145, 0.9);
    color: #fefefe;
    font-weight: 600;
    font-size: 12px;
    border-radius: 5px;
    white-space: nowrap;
    box-shadow: 0 0 6px rgba(11, 61, 145, 0.5);
    display: none;
    user-select: none;
    z-index: 1000;
  }}
</style>
</head>
<body>
  <nav id="legend" role="list" aria-label="Lista de municípios da Região Metropolitana de Campinas">
    <strong>Selecione um município:</strong>
    <div id="mun-list" tabindex="0"></div>
  </nav>

  <main id="map" role="region" aria-label="Mapa interativo dos municípios da Região Metropolitana de Campinas">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"></svg>
    <div id="tooltip" role="tooltip" aria-hidden="true"></div>
  </main>

  <aside id="info-panel" role="region" aria-live="polite" aria-label="Informações do município selecionado">
    <h3>Selecione um município</h3>
    <div><strong>População:</strong> <span>-</span></div>
    <div><strong>Área:</strong> <span>-</span></div>
    <div><strong>PIB (2021):</strong> <span>-</span></div>
  </aside>

<script>
  const geojson = {geojson_str};
  const svg = document.querySelector("svg");
  const munList = document.getElementById("mun-list");
  const tooltip = document.getElementById("tooltip");
  const infoPanel = document.getElementById("info-panel");
  const mapDiv = document.getElementById("map");

  let selectedName = null;
  const paths = {{}};

  // Extrai coordenadas para projeção
  let allCoords = [];
  geojson.features.forEach(f => {{
    const geom = f.geometry;
    if (geom.type === "Polygon") {{
      geom.coordinates[0].forEach(c => allCoords.push(c));
    }} else if (geom.type === "MultiPolygon") {{
      geom.coordinates.forEach(poly => poly[0].forEach(c => allCoords.push(c)));
    }}
  }});

  const lons = allCoords.map(c => c[0]);
  const lats = allCoords.map(c => c[1]);
  const minLon = Math.min(...lons);
  const maxLon = Math.max(...lons);
  const minLat = Math.min(...lats);
  const maxLat = Math.max(...lats);

  // Função simples de projeção geográfica para coordenadas SVG
  function project(coord) {{
    const [lon, lat] = coord;
    const x = ((lon - minLon) / (maxLon - minLon)) * 900 + 50;
    const y = 900 - ((lat - minLat) / (maxLat - minLat)) * 850;
    return [x, y];
  }}

  // Converte array de coordenadas em path SVG
  function polygonToPath(coords) {{
    return coords.map(c => {{
      const [x, y] = project(c);
      return x + "," + y;
    }}).join(" ");
  }}

  // Formata número para o padrão pt-BR
  function formatNumber(num) {{
    if(num === null || num === undefined) return "N/A";
    return num.toLocaleString('pt-BR');
  }}

  // Atualiza o painel de informações com dados do município
  function updateInfoPanel(data) {{
    if(!data) {{
      infoPanel.querySelector('h3').textContent = "Selecione um município";
      infoPanel.querySelectorAll('div span').forEach(span => span.textContent = "-");
      return;
    }}
    infoPanel.querySelector('h3').textContent = data.name;
    const spans = infoPanel.querySelectorAll('div span');
    spans[0].textContent = formatNumber(data.populacao);
    spans[1].textContent = data.area ? data.area.toFixed(1) + " km²" : "N/A";
    spans[2].textContent = data.pib_2021 ? "R$ " + formatNumber(data.pib_2021) : "N/A";
  }}

  // Limpa realce de todos polígonos
  function clearHighlight() {{
    Object.values(paths).forEach(p => p.classList.remove("highlight"));
  }}

  // Limpa seleção de todos polígonos
  function clearSelection() {{
    Object.values(paths).forEach(p => p.classList.remove("selected"));
  }}

  // Atualiza estilo ativo da legenda
  function setActiveLegend(name) {{
    Array.from(munList.children).forEach(child => {{
      child.classList.toggle("active", child.dataset.name === name);
    }});
  }}

  // Seleciona município
  function selectMunicipio(name) {{
    clearHighlight();
    clearSelection();
    if(paths[name]) paths[name].classList.add("selected");
    setActiveLegend(name);
    selectedName = name;

    const data = geojson.features.find(f => f.properties.name === name);
    if (data) {{
      updateInfoPanel(data.properties);
    }}
  }}

  // Criando polígonos SVG e itens da legenda
  geojson.features.forEach(f => {{
    const props = f.properties;
    const name = props.name;
    const geom = f.geometry;
    let pathD = "";

    if (geom.type === "Polygon") {{
      pathD = "M" + polygonToPath(geom.coordinates[0]) + " Z";
    }} else if (geom.type === "MultiPolygon") {{
      geom.coordinates.forEach(poly => {{
        pathD += "M" + polygonToPath(poly[0]) + " Z";
      }});
    }}

    const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathEl.setAttribute("d", pathD);
    pathEl.classList.add("polygon");
    pathEl.setAttribute("data-name", name);

    svg.appendChild(pathEl);
    paths[name] = pathEl;

    // Eventos para tooltip e seleção
    pathEl.addEventListener("mousemove", (e) => {{
      tooltip.style.display = "block";
      tooltip.textContent = name;
      const mapRect = mapDiv.getBoundingClientRect();
      let left = e.clientX - mapRect.left + 10;
      let top = e.clientY - mapRect.top + 10;

      if(left + tooltip.offsetWidth > mapRect.width) {{
        left = e.clientX - mapRect.left - tooltip.offsetWidth - 8;
      }}
      if(top + tooltip.offsetHeight > mapRect.height) {{
        top = e.clientY - mapRect.top - tooltip.offsetHeight - 8;
      }}

      tooltip.style.left = left + "px";
      tooltip.style.top = top + "px";

      clearHighlight();
      if (!pathEl.classList.contains("selected")) {{
        pathEl.classList.add("highlight");
      }}
    }});

    pathEl.addEventListener("mouseleave", () => {{
      tooltip.style.display = "none";
      clearHighlight();
    }});

    pathEl.addEventListener("click", () => {{
      selectMunicipio(name);
    }});

    // Cria item da legenda
    const legendItem = document.createElement("div");
    legendItem.textContent = name;
    legendItem.dataset.name = name;
    munList.appendChild(legendItem);

    legendItem.addEventListener("mouseenter", () => {{
      clearHighlight();
      if(paths[name] && !paths[name].classList.contains("selected")) paths[name].classList.add("highlight");
    }});
    legendItem.addEventListener("mouseleave", () => {{
      clearHighlight();
    }});
    legendItem.addEventListener("click", () => {{
      selectMunicipio(name);
    }});
  }});
</script>

</body>
</html>
"""

# Renderiza o HTML no Streamlit
st.components.v1.html(html_code, height=650, scrolling=True)
