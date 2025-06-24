import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# === Configurações de página ===
st.set_page_config(
    page_title='RMC Data - Mapa Interativo',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# === Títulos ===
st.markdown('# RMC Data')
st.markdown('## Indicadores da Região Metropolitana de Campinas')

# === Carregar shapefile e dados ===
gdf = gpd.read_file('./shapefile_rmc/RMC_municipios.shp')
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

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

# === HTML + CSS + JS ===
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC - Transparência</title>
<style>
  /* Reset e base */
  *, *::before, *::after {{
    box-sizing: border-box;
  }}
  html, body {{
    margin: 0; padding: 0;
    height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    background: #f9fafb;
    color: #222;
    overflow: hidden;
    display: flex;
    flex-direction: row;
    gap: 16px;
    padding: 12px 18px;
  }}

  /* === LEGEND === */
  #legend {{
    width: 260px;
    background: #fff;
    padding: 20px 16px 20px 22px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.07);
    border-radius: 12px;
    overflow-y: auto;
    user-select: none;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
  }}
  #legend strong {{
    font-weight: 800;
    font-size: 20px;
    color: #0b3d91;
    margin-bottom: 14px;
    border-bottom: 3px solid #0b3d91;
    padding-bottom: 8px;
  }}
  #search-box {{
    margin-bottom: 16px;
    padding: 8px 12px;
    font-size: 15px;
    border: 1.8px solid #0b3d91;
    border-radius: 8px;
    outline-offset: 2px;
    transition: box-shadow 0.3s ease;
  }}
  #search-box:focus {{
    box-shadow: 0 0 6px #0b3d91aa;
    border-color: #08318d;
  }}
  #mun-list {{
    flex-grow: 1;
    overflow-y: auto;
  }}
  #mun-list div {{
    padding: 8px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
    font-size: 15px;
    color: #3a3a3a;
    white-space: nowrap;
  }}
  #mun-list div:hover {{
    background-color: #d5e1fc;
    color: #08318d;
  }}
  #mun-list div.active {{
    background-color: #0b3d91;
    color: #fff;
    font-weight: 700;
  }}

  /* === MAP CONTAINER === */
  #map {{
    flex-grow: 1;
    position: relative;
    background: #fff;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    border-radius: 12px;
    overflow: hidden;
    user-select: none;
  }}
  svg {{
    width: 100%;
    height: 100vh;
    display: block;
  }}

  /* === INFO PANEL === */
  #info-panel {{
    width: 340px;
    max-height: 100vh;
    background: #fff;
    padding: 24px 30px 42px 30px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.13);
    color: #333;
    font-size: 16px;
    line-height: 1.5;
    overflow-y: auto;
    border-radius: 12px;
    position: relative;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    opacity: 0;
    transform: translateX(30px);
    pointer-events: none;
    transition: opacity 0.35s ease, transform 0.35s ease;
  }}
  #info-panel.visible {{
    opacity: 1;
    transform: translateX(0);
    pointer-events: auto;
  }}
  #info-panel h3 {{
    margin-top: 0;
    font-weight: 900;
    font-size: 22px;
    color: #0b3d91;
    border-bottom: 3px solid #0b3d91;
    padding-bottom: 10px;
    margin-bottom: 24px;
    user-select: text;
  }}

  /* Label e valor em coluna */
  #info-panel div.info-row {{
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
  }}
  #info-panel div.info-row strong {{
    color: #0b3d91;
    margin-bottom: 8px;
    user-select: text;
  }}
  #info-panel div.info-row span {{
    color: #333;
    font-weight: 600;
    font-size: 1.05rem;
    user-select: text;
  }}

  /* Botão fechar painel info */
  #info-panel button#close-info {{
    position: absolute;
    top: 18px;
    right: 22px;
    background: transparent;
    border: none;
    font-size: 30px;
    color: #0b3d91;
    cursor: pointer;
    font-weight: 900;
    line-height: 1;
    padding: 0;
    transition: color 0.25s ease;
  }}
  #info-panel button#close-info:hover {{
    color: #08318d;
  }}

  /* Fonte discreta rodapé painel info */
  #info-panel footer {{
    margin-top: auto;
    font-size: 13px;
    font-weight: 400;
    color: #666;
    opacity: 0.55;
    text-align: right;
    font-style: italic;
    user-select: none;
  }}

  /* === Polígonos do mapa === */
  .polygon {{
    fill: rgba(11, 61, 145, 0.18);
    stroke: rgba(11, 61, 145, 0.7);
    stroke-width: 1.1;
    cursor: pointer;
    transition: fill 0.3s ease, stroke 0.3s ease;
    opacity: 0.9;
  }}
  .polygon:hover {{
    fill: rgba(11, 61, 145, 0.4);
    stroke-width: 2.2;
    filter: drop-shadow(0 0 7px rgba(11, 61, 145, 0.4));
  }}
  .polygon.selected {{
    fill: rgba(11, 61, 145, 0.6);
    stroke: rgba(11, 61, 145, 0.95);
    stroke-width: 2.8;
    filter: drop-shadow(0 0 12px rgba(11, 61, 145, 0.7));
  }}

  /* Tooltip */
  #tooltip {{
    position: absolute;
    pointer-events: none;
    padding: 8px 16px;
    background: rgba(11, 61, 145, 0.92);
    color: #fefefe;
    font-weight: 700;
    font-size: 13px;
    border-radius: 6px;
    white-space: nowrap;
    box-shadow: 0 0 10px rgba(11, 61, 145, 0.75);
    display: none;
    user-select: none;
    z-index: 1100;
    transition: opacity 0.2s ease;
    opacity: 0;
  }}
  #tooltip.visible {{
    display: block;
    opacity: 1;
  }}
</style>
</head>
<body>
  <nav id="legend" role="list" aria-label="Lista de municípios da Região Metropolitana de Campinas">
    <strong>Municípios da RMC</strong>
    <input type="search" id="search-box" placeholder="Buscar município..." aria-label="Buscar município" />
    <div id="mun-list" tabindex="0" role="listbox" aria-multiselectable="false"></div>
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
  (function() {{
    const geojson = {geojson_str};
    const svg = document.querySelector("svg");
    const munList = document.getElementById("mun-list");
    const tooltip = document.getElementById("tooltip");
    const infoPanel = document.getElementById("info-panel");
    const closeBtn = document.getElementById("close-info");
    const mapDiv = document.getElementById("map");
    const searchBox = document.getElementById("search-box");

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

    // Limpa realce e seleção
    function clearHighlight() {{
      Object.values(paths).forEach(p => p.classList.remove("highlight"));
    }}
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

    // Fecha painel info
    closeBtn.addEventListener("click", () => {{
      infoPanel.classList.remove("visible");
      clearSelection();
      setActiveLegend(null);
      selectedName = null;
    }});

    // Criar polígonos SVG e itens da legenda (delegação para performance)
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

      // Criar item legenda
      const div = document.createElement("div");
      div.textContent = name;
      div.dataset.name = name;
      munList.appendChild(div);
    }});

    // Evento click em legenda (delegação)
    munList.addEventListener("click", (e) => {{
      if(e.target && e.target.dataset && e.target.dataset.name) {{
        selectMunicipio(e.target.dataset.name);
      }}
    }});
    munList.addEventListener("keydown", (e) => {{
      if(e.key === "Enter" && e.target && e.target.dataset && e.target.dataset.name) {{
        selectMunicipio(e.target.dataset.name);
      }}
    }});

    // Evento mouse nos polígonos
    svg.addEventListener("mousemove", (e) => {{
      const target = e.target;
      if(target && target.classList.contains("polygon")) {{
        const name = target.dataset.name;
        if(name) {{
          tooltip.textContent = name;
          tooltip.style.left = (e.clientX + 16) + "px";
          tooltip.style.top = (e.clientY + 16) + "px";
          tooltip.classList.add("visible");
          tooltip.setAttribute("aria-hidden", "false");
          // Sutil realce
          clearHighlight();
          if(name !== selectedName) {{
            target.classList.add("highlight");
          }}
        }}
      }} else {{
        tooltip.classList.remove("visible");
        tooltip.setAttribute("aria-hidden", "true");
        clearHighlight();
      }}
    }});

    // Ocultar tooltip ao sair do svg
    svg.addEventListener("mouseleave", () => {{
      tooltip.classList.remove("visible");
      tooltip.setAttribute("aria-hidden", "true");
      clearHighlight();
    }});

    // Clique no mapa - seleciona
    svg.addEventListener("click", (e) => {{
      const target = e.target;
      if(target && target.classList.contains("polygon")) {{
        selectMunicipio(target.dataset.name);
      }}
    }});

    // Busca no input - filtro legenda e mapa
    searchBox.addEventListener("input", () => {{
      const val = searchBox.value.toLowerCase().trim();
      Array.from(munList.children).forEach(div => {{
        const visible = div.dataset.name.toLowerCase().includes(val);
        div.style.display = visible ? "block" : "none";
        if(paths[div.dataset.name]) {{
          paths[div.dataset.name].style.display = visible ? "inline" : "none";
        }}
      }});
    }});

    // Inicializa sem seleção e foco no campo de busca
    searchBox.focus();
    updateInfoPanel(null);
  }})();
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=700, scrolling=True)
