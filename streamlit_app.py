import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# CONFIGURAÇÕES DA PÁGINA INICIAL
st.set_page_config(
    page_title='RMC Data',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# TÍTULO
st.markdown('# RMC Data')
st.markdown('## Dados e indicadores da Região Metropolitana de Campinas')

# SHAPEFILE
gdf = gpd.read_file('./shapefile_rmc/RMC_municipios.shp')
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

# DADOS DO SHAPEFILE
df_dados = pd.read_excel('dados_rmc.xlsx')
df_dados.set_index("nome", inplace=True)

features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__

    if nome in df_dados.index:
        dados = df_dados.loc[nome]
        feature_props = {
            "name": nome,
            "pib_2021": dados["pib_2021"],
            "participacao_rmc": dados["participacao_rmc"],
            "pib_per_capita": dados["per_capita_2021"],
            "populacao": dados["populacao_2022"],
            "area": dados["area"],
            "densidade_demografica": dados["densidade_demografica_2022"]
        }
    else:
        feature_props = {
            "name": nome,
            "pib_2021": None,
            "participacao_rmc": None,
            "pib_per_capita": None,
            "populacao": None,
            "area": None,
            "densidade_demografica": None
        }

    features.append({
        "type": "Feature",
        "properties": feature_props,
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
    background-color: transparent;
    color: #222;
    overflow: hidden;
    display: flex;
    flex-direction: row;
    gap: 12px;
    padding: 12px 16px;
  }}

  /* === LEGEND === */
  #legend {{
    width: 240px;
    background: #fff;
    padding: 20px 16px 20px 20px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.06);
    border-radius: 10px;
    overflow-y: auto;
    user-select: none;
    flex-shrink: 0;
  }}
  #legend strong {{
    display: block;
    font-weight: 700;
    font-size: 18px;
    margin-bottom: 14px;
    color: #0b3d91;
    border-bottom: 2px solid #0b3d91;
    padding-bottom: 6px;
  }}
  #legend div {{
    margin-bottom: 10px;
    padding: 8px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
    color: #3a3a3a;
    font-size: 14px;
    white-space: nowrap;
  }}
  #legend div:hover {{
    background-color: #e3eafc;
    color: #08318d;
  }}
  #legend div.active {{
    background-color: #0b3d91;
    color: #fff;
    font-weight: 700;
  }}

  /* === MAP CONTAINER === */
  #map {{
    flex-grow: 1;
    position: relative;
    background: #fff;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.07);
    border-radius: 10px;
    overflow: hidden;
    user-select: none;
  }}
  svg {{
    width: 100%;
    height: 100vh;
    display: block;
    user-select: none;
  }}

  /* === INFO PANEL === */
  #info-panel {{
    width: 320px;
    max-height: 100vh;
    background: #fff;
    padding: 22px 26px 36px 26px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.12);
    color: #333;
    font-size: 15px;
    line-height: 1.5;
    overflow-y: auto;
    border-radius: 10px;
    position: relative;
    flex-shrink: 0;
    display: none; /* inicia escondido */
    flex-direction: column;
  }}
  #info-panel.visible {{
    display: flex;
  }}
  #info-panel h3 {{
    margin-top: 0;
    font-weight: 700;
    font-size: 20px;
    color: #0b3d91;
    border-bottom: 2px solid #0b3d91;
    padding-bottom: 10px;
    margin-bottom: 20px;
  }}

  /* Label e valor em coluna */
  #info-panel div.info-row {{
    margin-bottom: 18px;
    display: flex;
    flex-direction: column;
  }}
  #info-panel div.info-row strong {{
    display: block;
    color: #0b3d91;
    margin-bottom: 6px;
    white-space: normal;
  }}
  #info-panel div.info-row span {{
    color: #333;
    font-weight: 600;
    font-size: 1rem;
    white-space: normal;
  }}

  /* Botão fechar painel info */
  #info-panel button#close-info {{
    position: absolute;
    top: 14px;
    right: 18px;
    background: transparent;
    border: none;
    font-size: 26px;
    color: #0b3d91;
    cursor: pointer;
    font-weight: 900;
    line-height: 1;
    padding: 0;
    transition: color 0.3s ease;
  }}
  #info-panel button#close-info:hover {{
    color: #08318d;
  }}

  /* Fonte discreta rodapé painel info */
  #info-panel footer {{
    margin-top: auto;
    font-size: 12px;
    font-weight: 400;
    color: #666;
    opacity: 0.6;
    text-align: right;
    font-style: italic;
  }}

  /* === Polígonos do mapa === */
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
    padding: 6px 14px;
    background: rgba(11, 61, 145, 0.9);
    color: #fefefe;
    font-weight: 600;
    font-size: 12px;
    border-radius: 5px;
    white-space: nowrap;
    box-shadow: 0 0 8px rgba(11, 61, 145, 0.7);
    display: none;
    user-select: none;
    z-index: 1000;
  }}
</style>
</head>
<body>
  <nav id="legend" role="list" aria-label="Lista de municípios da Região Metropolitana de Campinas">
    <strong>Municípios da RMC</strong>
    <div id="mun-list" tabindex="0"></div>
  </nav>

  <main id="map" role="region" aria-label="Mapa interativo dos municípios da Região Metropolitana de Campinas">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"></svg>
    <div id="tooltip" role="tooltip" aria-hidden="true"></div>
  </main>

  <aside id="info-panel" role="region" aria-live="polite" aria-label="Informações do município selecionado">
    <button id="close-info" aria-label="Fechar painel de informações">&times;</button>
    <h3>Selecione um município</h3>
    <div class="info-row"><strong>PIB (2021):</strong> <span>-</span></div>
    <div class="info-row"><strong>Participação na RMC:</strong> <span>-</span></div>
    <div class="info-row"><strong>PIB per capita (2021):</strong> <span>-</span></div>
    <div class="info-row"><strong>População:</strong> <span>-</span></div>
    <div class="info-row"><strong>Área:</strong> <span>-</span></div>
    <div class="info-row"><strong>Densidade demográfica (2022):</strong> <span>-</span></div>
    <footer>Fonte: IBGE Cidades</footer>
  </aside>

<script>
  const geojson = {geojson_str};
  const svg = document.querySelector("svg");
  const munList = document.getElementById("mun-list");
  const tooltip = document.getElementById("tooltip");
  const infoPanel = document.getElementById("info-panel");
  const closeBtn = document.getElementById("close-info");
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

  // Projeção geográfica simples para SVG
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

  // Formata número para pt-BR
  function formatNumberBR(num, decimals = 2) {{
    if (num === null || num === undefined) return "-";
    return num.toLocaleString('pt-BR', {{ minimumFractionDigits: decimals, maximumFractionDigits: decimals }});
  }}

  // Atualiza painel de informações
  function updateInfoPanel(data) {{
    if(!data) {{
      infoPanel.querySelector('h3').textContent = "Selecione um município";
      infoPanel.querySelectorAll('div.info-row span').forEach(span => span.textContent = "-");
      infoPanel.classList.remove("visible");
      return;
    }}
    infoPanel.querySelector('h3').textContent = data.name || "-";

    const spans = infoPanel.querySelectorAll('div.info-row span');

    spans[0].textContent = data.pib_2021 ? "R$ " + formatNumberBR(data.pib_2021, 0) : "-";
    spans[1].textContent = data.participacao_rmc
      ? (data.participacao_rmc * 100).toFixed(2).replace('.', ',') + '%'
      : "-";
    spans[2].textContent = data.pib_per_capita ? "R$ " + formatNumberBR(data.pib_per_capita, 2) : "-";
    spans[3].textContent = data.populacao ? formatNumberBR(data.populacao, 0) : "-";
    spans[4].textContent = data.area ? data.area.toFixed(1).replace('.', ',') + " km²" : "-";
    spans[5].textContent = data.densidade_demografica
      ? formatNumberBR(data.densidade_demografica, 2) + " hab/km²"
      : "-";

    infoPanel.classList.add("visible");
  }}

  // Limpa realce dos polígonos
  function clearHighlight() {{
    Object.values(paths).forEach(p => p.classList.remove("highlight"));
  }}

  // Limpa seleção dos polígonos
  function clearSelection() {{
    Object.values(paths).forEach(p => p.classList.remove("selected"));
  }}

  // Atualiza a legenda com o ativo
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

  // Fecha painel info
  closeBtn.addEventListener("click", () => {{
    infoPanel.classList.remove("visible");
    clearSelection();
    setActiveLegend(null);
    selectedName = null;
  }});

  // Cria polígonos e itens da legenda
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

    // Tooltip e seleção
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

    // Item legenda
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
st.components.v1.html(html_code, height=680, scrolling=True)
