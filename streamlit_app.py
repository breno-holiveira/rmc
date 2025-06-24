import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="Mapa RMC - Profissional Fino", layout="wide", page_icon="🗺️")

# Carregar shapefile e dados
gdf = gpd.read_file('./shapefile_rmc/RMC_municipios.shp')
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values('NM_MUN')

df_dados = pd.read_excel('dados_rmc.xlsx')
df_dados.set_index("nome", inplace=True)

features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__

    props = {
        "name": nome,
        "pib_2021": None,
        "participacao_rmc": None,
        "pib_per_capita": None,
        "populacao": None,
        "area": None,
        "densidade_demografica": None
    }

    if nome in df_dados.index:
        dados = df_dados.loc[nome]
        props.update({
            "pib_2021": dados["pib_2021"],
            "participacao_rmc": dados["participacao_rmc"],
            "pib_per_capita": dados["per_capita_2021"],
            "populacao": dados["populacao_2022"],
            "area": dados["area"],
            "densidade_demografica": dados["densidade_demografica_2022"],
        })

    features.append({
        "type": "Feature",
        "properties": props,
        "geometry": geom
    })

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC - Profissional Fino</title>
<style>
  /* RESET */
  *, *::before, *::after {{
    box-sizing: border-box;
  }}
  html, body {{
    margin: 0; padding: 0;
    height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background: #f5f7fa;
    color: #34495e;
    overflow: hidden;
  }}

  /* GRID LAYOUT PRINCIPAL */
  body {{
    display: grid;
    grid-template-columns: 320px 1fr 400px;
    grid-template-rows: auto 1fr;
    grid-template-areas:
      "header header header"
      "sidebar map info";
    height: 100vh;
    gap: 20px;
    padding: 22px 26px;
  }}

  header {{
    grid-area: header;
    font-weight: 700;
    font-size: 26px;
    color: #2c3e50;
    border-bottom: 1px solid #dce4ec;
    padding-bottom: 10px;
    user-select: none;
    font-variant: small-caps;
    letter-spacing: 1.1px;
  }}

  /* SIDEBAR (LEGENDA) - NOVA LEGENDA */
  nav#sidebar {{
    grid-area: sidebar;
    background: rgba(255 255 255 / 0.92);
    border-radius: 16px;
    padding: 24px 22px;
    box-shadow: 0 6px 18px rgb(41 128 185 / 0.12);
    display: flex;
    flex-direction: column;
    font-size: 16px;
    color: #34495e;
  }}
  nav#sidebar > strong {{
    font-size: 22px;
    font-weight: 700;
    color: #2980b9;
    margin-bottom: 20px;
    border-bottom: 3px solid #2980b9aa;
    padding-bottom: 8px;
  }}
  #search-box {{
    padding: 11px 16px;
    font-size: 16px;
    border: 1.4px solid #a3b1c6;
    border-radius: 12px;
    outline-offset: 2px;
    background: #fefefe;
    font-weight: 600;
    color: #34495e;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 22px;
    user-select: text;
  }}
  #search-box::placeholder {{
    color: #a3b1c6;
    font-weight: 500;
  }}
  #search-box:focus {{
    border-color: #2980b9;
    box-shadow: 0 0 10px #5dade2cc;
  }}
  #mun-list {{
    overflow-y: auto;
    flex-grow: 1;
    scrollbar-width: thin;
    scrollbar-color: #a3b1c6 transparent;
  }}
  #mun-list::-webkit-scrollbar {{
    width: 7px;
  }}
  #mun-list::-webkit-scrollbar-thumb {{
    background-color: #a3b1c6;
    border-radius: 5px;
  }}
  #mun-list > div {{
    padding: 12px 20px;
    border-radius: 12px;
    margin-bottom: 9px;
    cursor: pointer;
    font-weight: 600;
    color: #34495e;
    transition: background-color 0.35s ease, color 0.35s ease;
    user-select: none;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }}
  #mun-list > div:hover {{
    background-color: #d8e9ffcc;
    color: #2980b9;
  }}
  #mun-list > div.active {{
    background-color: #2980b9;
    color: #fff;
    font-weight: 700;
  }}

  /* MAPA CENTRAL */
  main#map {{
    grid-area: map;
    position: relative;
    background: #ffffffdd;
    border-radius: 18px;
    box-shadow: 0 8px 32px rgb(41 128 185 / 0.08);
    user-select: none;
    overflow: hidden;
  }}
  svg {{
    width: 100%;
    height: 100vh;
    display: block;
  }}

  /* TOOLTIP */
  #tooltip {{
    position: absolute;
    pointer-events: none;
    padding: 8px 18px;
    background: rgba(41, 128, 185, 0.88);
    color: #fefefe;
    font-weight: 600;
    font-size: 14px;
    border-radius: 10px;
    white-space: nowrap;
    box-shadow: 0 0 14px rgba(41, 128, 185, 0.35);
    opacity: 0;
    transition: opacity 0.3s ease;
    user-select: none;
    z-index: 1100;
  }}
  #tooltip.visible {{
    opacity: 1;
  }}

  /* PAINEL INFO (DADOS) */
  aside#info {{
    grid-area: info;
    background: rgba(255 255 255 / 0.92);
    border-radius: 18px;
    padding: 32px 30px 44px 30px;
    box-shadow: 0 10px 38px rgb(41 128 185 / 0.13);
    color: #34495e;
    font-size: 16px;
    line-height: 1.55;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    user-select: text;
    position: relative;
  }}
  aside#info h3 {{
    font-weight: 900;
    font-size: 26px;
    color: #2471a3;
    margin: 0 0 28px 0;
    border-bottom: 2.5px solid #2471a3aa;
    padding-bottom: 12px;
  }}
  aside#info .info-row {{
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
  }}
  aside#info .info-row strong {{
    font-weight: 700;
    color: #2471a3;
  }}
  aside#info .info-row span {{
    font-weight: 600;
  }}
  aside#info footer {{
    margin-top: auto;
    font-size: 13px;
    font-weight: 400;
    color: #7f8c8d;
    opacity: 0.6;
    text-align: right;
    font-style: italic;
    user-select: none;
  }}

  /* POLÍGONOS DO MAPA */
  .polygon {{
    fill: rgba(41, 128, 185, 0.16);
    stroke: rgba(41, 128, 185, 0.7);
    stroke-width: 1.2;
    cursor: pointer;
    transition: fill 0.3s ease, stroke 0.3s ease, filter 0.3s ease;
    opacity: 0.85;
  }}
  .polygon:hover {{
    fill: rgba(41, 128, 185, 0.38);
    stroke-width: 2.3;
    filter: drop-shadow(0 0 8px rgba(41, 128, 185, 0.3));
  }}
  .polygon.selected {{
    fill: rgba(41, 128, 185, 0.53);
    stroke: rgba(41, 128, 185, 0.98);
    stroke-width: 3;
    filter: drop-shadow(0 0 16px rgba(41, 128, 185, 0.55));
  }}

  /* Scrollbars customizados */
  #info::-webkit-scrollbar {{
    width: 8px;
  }}
  #info::-webkit-scrollbar-thumb {{
    background-color: #a3b1c6cc;
    border-radius: 5px;
  }}
  #info::-webkit-scrollbar-track {{
    background: transparent;
  }}

  /* Responsividade */
  @media (max-width: 1150px) {{
    body {{
      grid-template-columns: 280px 1fr;
      grid-template-areas:
        "header header"
        "sidebar map";
    }}
    aside#info {{
      display: none;
    }}
  }}
</style>
</head>
<body>
  <header>Região Metropolitana de Campinas - Dados e Indicadores</header>

  <nav id="sidebar" aria-label="Lista de municípios da RMC">
    <strong>Municípios</strong>
    <input type="search" id="search-box" placeholder="Buscar município..." autocomplete="off" aria-label="Buscar município"/>
    <div id="mun-list" tabindex="0" role="listbox" aria-multiselectable="false" aria-label="Lista de municípios"></div>
  </nav>

  <main id="map" role="region" aria-label="Mapa interativo da Região Metropolitana de Campinas">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"></svg>
    <div id="tooltip" role="tooltip" aria-hidden="true"></div>
  </main>

  <aside id="info" role="region" aria-live="polite" aria-label="Informações do município selecionado">
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
    const infoPanel = document.getElementById("info");
    const searchBox = document.getElementById("search-box");

    let selectedName = null;
    const paths = {{}};

    // Projeção simples para SVG
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

    function project(coord) {{
      const [lon, lat] = coord;
      const x = ((lon - minLon) / (maxLon - minLon)) * 900 + 50;
      const y = 900 - ((lat - minLat) / (maxLat - minLat)) * 850;
      return [x, y];
    }}

    function polygonToPath(coords) {{
      return coords.map(c => {{
        const [x, y] = project(c);
        return x + "," + y;
      }}).join(" ");
    }}

    function formatNumberBR(num, decimals=2) {{
      if(num === null || num === undefined) return "-";
      return num.toLocaleString('pt-BR', {{ minimumFractionDigits: decimals, maximumFractionDigits: decimals }});
    }}

    function updateInfo(data) {{
      if(!data) {{
        infoPanel.querySelector('h3').textContent = "Selecione um município";
        infoPanel.querySelectorAll('div.info-row span').forEach(s => s.textContent = "-");
        return;
      }}
      infoPanel.querySelector('h3').textContent = data.name || "-";
      const spans = infoPanel.querySelectorAll('div.info-row span');

      spans[0].textContent = data.pib_2021 ? "R$ " + formatNumberBR(data.pib_2021, 0) : "-";
      spans[1].textContent = data.participacao_rmc ? (data.participacao_rmc*100).toFixed(2).replace('.', ',') + '%' : "-";
      spans[2].textContent = data.pib_per_capita ? "R$ " + formatNumberBR(data.pib_per_capita, 2) : "-";
      spans[3].textContent = data.populacao ? formatNumberBR(data.populacao, 0) : "-";
      spans[4].textContent = data.area ? data.area.toFixed(1).replace('.', ',') + " km²" : "-";
      spans[5].textContent = data.densidade_demografica ? formatNumberBR(data.densidade_demografica, 2) + " hab/km²" : "-";
    }}

    function clearHighlight() {{
      Object.values(paths).forEach(p => p.classList.remove("highlight"));
    }}

    function clearSelection() {{
      Object.values(paths).forEach(p => p.classList.remove("selected"));
    }}

    function setActiveLegend(name) {{
      Array.from(munList.children).forEach(div => {{
        div.classList.toggle("active", div.dataset.name === name);
      }});
    }}

    function selectMunicipio(name) {{
      clearHighlight();
      clearSelection();
      if(paths[name]) paths[name].classList.add("selected");
      setActiveLegend(name);
      selectedName = name;
      const f = geojson.features.find(feat => feat.properties.name === name);
      if(f) updateInfo(f.properties);
    }}

    // Criar polígonos SVG e itens legenda (delegação)
    geojson.features.forEach(f => {{
      const name = f.properties.name;
      const geom = f.geometry;

      let path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.classList.add("polygon");
      path.setAttribute("data-name", name);

      if(geom.type === "Polygon") {{
        path.setAttribute("d", "M" + polygonToPath(geom.coordinates[0]) + " Z");
      }} else if(geom.type === "MultiPolygon") {{
        const d = geom.coordinates.map(poly => "M" + polygonToPath(poly[0]) + " Z").join(" ");
        path.setAttribute("d", d);
      }}

      svg.appendChild(path);
      paths[name] = path;

      const div = document.createElement("div");
      div.textContent = name;
      div.dataset.name = name;
      div.setAttribute("role", "option");
      div.tabIndex = 0;
      munList.appendChild(div);
    }});

    // Eventos legenda - clique e teclado
    munList.addEventListener("click", e => {{
      if(e.target.dataset.name) selectMunicipio(e.target.dataset.name);
    }});
    munList.addEventListener("keydown", e => {{
      if(e.key === "Enter" && e.target.dataset.name) selectMunicipio(e.target.dataset.name);
    }});

    // Tooltip
    svg.addEventListener("mousemove", e => {{
      if(e.target.classList.contains("polygon")) {{
        tooltip.textContent = e.target.dataset.name;
        tooltip.style.left = (e.clientX + 16) + "px";
        tooltip.style.top = (e.clientY + 16) + "px";
        tooltip.classList.add("visible");
        e.target.classList.add("highlight");
      }} else {{
        tooltip.classList.remove("visible");
        clearHighlight();
      }}
    }});
    svg.addEventListener("mouseleave", e => {{
      tooltip.classList.remove("visible");
      clearHighlight();
    }});

    // Clique no polígono
    svg.addEventListener("click", e => {{
      if(e.target.classList.contains("polygon")) {{
        selectMunicipio(e.target.dataset.name);
      }}
    }});

    // Busca na legenda
    searchBox.addEventListener("input", e => {{
      const val = e.target.value.toLowerCase();
      Array.from(munList.children).forEach(div => {{
        div.style.display = div.textContent.toLowerCase().includes(val) ? "" : "none";
      }});
    }});

    // Seleciona automaticamente o primeiro município na lista
    if(geojson.features.length > 0) {{
      selectMunicipio(geojson.features[0].properties.name);
      // Scroll para o ativo
      const firstActive = munList.querySelector("div.active");
      if(firstActive) firstActive.scrollIntoView({{behavior: "smooth", block: "center"}});
    }}
  }})();
</script>
</body>
</html>
"""

st.components.v1.html(html_code, height=940, scrolling=True)
