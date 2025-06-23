import streamlit as st
import geopandas as gpd
import json
import streamlit.components.v1 as components

st.title('Data')

st.set_page_config(layout="wide")

st.header('Dados e indicadores da Região Metropolitana de Campinas')

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

gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
gdf = gdf.sort_values(by="NM_MUN")

geojson = {"type": "FeatureCollection", "features": []}
for _, row in gdf.iterrows():
    name = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    extra = dados_extra.get(name, {"populacao": None, "area": None, "pib_2021": None})
    geojson["features"].append({
        "type": "Feature",
        "properties": {
            "name": name,
            "populacao": extra["populacao"],
            "area": extra["area"],
            "pib_2021": extra["pib_2021"],
        },
        "geometry": geom
    })

geojson_str = json.dumps(geojson)

html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC - Transparência</title>
<style>
  html, body {
    margin: 0; padding: 0;
    height: 100vh;
    background-color: #fefefe;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    color: #333;
    user-select: none;
    display: flex;
    flex-direction: row;
    overflow: hidden;
  }

  /* Barra lateral esquerda - lista municípios */
  #legend {
    width: 220px;
    background-color: #fefefe;
    padding: 14px 16px;
    box-sizing: border-box;
    overflow-y: auto;
    border-radius: 10px 0 0 10px;
    box-shadow: inset 0 0 0px;
    font-size: 13px;
    line-height: 1.3;
    color: #444;
    flex-shrink: 0;
  }

  #legend strong {
    font-size: 14px;
    color: #222;
    margin-bottom: 12px;
    display: block;
    font-weight: 600;
    padding-bottom: 8px;
  }

  #legend div {
    padding: 6px 10px;
    margin-bottom: 5px;
    border-radius: 5px;
    cursor: pointer;
    color: #555;
    transition: background-color 0.3s ease, color 0.3s ease;
  }

  #legend div:hover {
    background-color: #e6f0ff;
    color: #1a1a1a;
  }

  #legend div.active {
    background-color: #cfe2ff;
    color: #0d3b66;
    font-weight: 600;
  }

  /* Container central do mapa */
  #map {
    flex-grow: 1;
    position: relative;
    background: #fefefe;
    box-shadow: inset 0 0 0px #000c;
    border-radius: 0;
    min-width: 0; /* para scroll dentro do flex */
  }

  svg {
    width: 100%;
    height: 100vh;
    display: block;
    background: transparent;
  }

  .polygon {
    fill: rgba(70, 130, 180, 0.35);    /* Azul steel suave, translúcido */
    stroke: #4682b4;                   /* Azul steel médio para contorno */
    stroke-width: 1;
    opacity: 0.95;
    cursor: pointer;
    transition: stroke 0.3s ease, stroke-width 0.3s ease, fill 0.3s ease;
  }

  .polygon.highlight {
    fill: rgba(100, 149, 237, 0.55);   /* Azul cornflower mais claro no hover */
    stroke: #6495ed;                   /* Azul cornflower no contorno */
    stroke-width: 3;
    filter: drop-shadow(0 0 4px rgba(100, 149, 237, 0.6));
    opacity: 1;
  }

  .polygon.selected {
    fill: rgba(30, 144, 255, 0.6);     /* Azul dodger mais forte na seleção */
    stroke: #1e90ff;                   /* Azul dodger escuro no contorno */
    stroke-width: 3.4;
    filter: drop-shadow(0 0 4px rgba(30, 144, 255, 0.85));
    opacity: 1;
  }

  #tooltip {
    position: absolute;
    pointer-events: none;
    padding: 2px 6px;
    background: rgba(240, 248, 255, 0.95); /* quase branco com azul gelo */
    color: #111;
    font-weight: 500;
    font-size: 11px;
    border-radius: 4px;
    white-space: nowrap;
    box-shadow: 0 0 6px rgba(85, 153, 255, 0.25);
    display: none;
    user-select: none;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }

  /* Nova barra lateral direita - painel resumo */
  #info-panel {
    width: 220px;
    background: #fefefe;
    padding: 14px 16px;
    box-sizing: border-box;
    overflow-y: auto;
    border-radius: 0 10px 10px 0;
    box-shadow: inset 0 0 0px #111827cc;
    font-size: 13px;
    line-height: 1.4;
    color: #444;
    flex-shrink: 0;
  }

  #info-panel h3 {
    margin-top: 0;
    font-weight: 600;
    font-size: 15px;
    color: #222;
    border-bottom: 1px solid #ccc;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }

  #info-panel div {
    margin-bottom: 10px;
  }

  /* Scrollbar legendas e info */
  #legend::-webkit-scrollbar,
  #info-panel::-webkit-scrollbar {
    width: 6px;
  }
  #legend::-webkit-scrollbar-track,
  #info-panel::-webkit-scrollbar-track {
    background: transparent;
  }
  #legend::-webkit-scrollbar-thumb,
  #info-panel::-webkit-scrollbar-thumb {
    background-color: #c0c0c0;
    border-radius: 3px;
  }
  #legend::-webkit-scrollbar-thumb:hover,
  #info-panel::-webkit-scrollbar-thumb:hover {
    background-color: #a0a0a0;
  }
</style>
</head>
<body>

<div id="legend" role="list" aria-label="Lista de municípios da Região Metropolitana de Campinas">
  <strong>Selecione um município:</strong>
  <div id="mun-list"></div>
</div>

<div id="map" role="region" aria-label="Mapa interativo dos municípios da RMC">
  <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"></svg>
  <div id="tooltip" role="tooltip"></div>
</div>

<div id="info-panel" role="region" aria-live="polite" aria-label="Informações do município selecionado">
  <h3>Selecione um município</h3>
  <div><strong>População:</strong> -</div>
  <div><strong>Área:</strong> -</div>
  <div><strong>PIB (2021):</strong> -</div>
</div>

<script>
  const geojson = {geojson_str};
  const svg = document.querySelector("svg");
  const munList = document.getElementById("mun-list");
  const tooltip = document.getElementById("tooltip");
  const infoPanel = document.getElementById("info-panel");
  const mapDiv = document.getElementById("map");

  let selectedName = null;
const paths = {{}};

  let allCoords = [];
  geojson.features.forEach(f => {
    const geom = f.geometry;
    if (geom.type === "Polygon") {
      geom.coordinates[0].forEach(c => allCoords.push(c));
    } else if (geom.type === "MultiPolygon") {
      geom.coordinates.forEach(poly => poly[0].forEach(c => allCoords.push(c)));
    }
  });

  const lons = allCoords.map(c => c[0]);
  const lats = allCoords.map(c => c[1]);
  const minLon = Math.min(...lons);
  const maxLon = Math.max(...lons);
  const minLat = Math.min(...lats);
  const maxLat = Math.max(...lats);

  function project(coord) {
    const [lon, lat] = coord;
    const x = ((lon - minLon) / (maxLon - minLon)) * 900 + 50;
    const y = 900 - ((lat - minLat) / (maxLat - minLat)) * 850;
    return [x, y];
  }

  function polygonToPath(coords) {
    return coords.map(c => {
      const [x, y] = project(c);
      return x + "," + y;
    }).join(" ");
  }

  function formatNumber(num) {
    if(num === null || num === undefined) return "N/A";
    return num.toLocaleString('pt-BR');
  }

  function updateInfoPanel(data) {
    if(!data) {
      infoPanel.querySelector('h3').textContent = "Selecione um município";
      infoPanel.querySelectorAll('div').forEach(d => d.innerHTML = "<strong>–</strong>");
      return;
    }
    infoPanel.querySelector('h3').textContent = data.name;
    infoPanel.querySelectorAll('div')[0].innerHTML = `<strong>População:</strong> ${formatNumber(data.populacao)}`;
    infoPanel.querySelectorAll('div')[1].innerHTML = `<strong>Área:</strong> ${data.area ? data.area.toFixed(1) + " km²" : "N/A"}`;
    infoPanel.querySelectorAll('div')[2].innerHTML = `<strong>PIB (2021):</strong> ${data.pib_2021 ? "R$ " + formatNumber(data.pib_2021) : "N/A"}`;
  }

  function clearHighlight() {
    Object.values(paths).forEach(p => p.classList.remove("highlight"));
  }

  function clearSelection() {
    Object.values(paths).forEach(p => p.classList.remove("selected"));
  }

  function setActiveLegend(name) {
    const legendItems = munList.children;
    for(let i=0; i < legendItems.length; i++) {
      legendItems[i].classList.toggle("active", legendItems[i].dataset.name === name);
    }
  }

  function selectMunicipio(name) {
    clearHighlight();
    clearSelection();
    if(paths[name]) paths[name].classList.add("selected");
    setActiveLegend(name);
    selectedName = name;

    // Atualiza painel de informações
    const data = geojson.features.find(f => f.properties.name === name);
    if (data) {
      updateInfoPanel(data.properties);
    }
  }

  geojson.features.forEach(f => {
    const props = f.properties;
    const name = props.name;
    const geom = f.geometry;
    let pathD = "";

    if (geom.type === "Polygon") {
      const pathData = polygonToPath(geom.coordinates[0]);
      pathD = `M${pathData} Z`;
    } else if (geom.type === "MultiPolygon") {
      geom.coordinates.forEach(poly => {
        const pathData = polygonToPath(poly[0]);
        pathD += `M${pathData} Z`;
      });
    }

    const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathEl.setAttribute("d", pathD);
    pathEl.classList.add("polygon");
    pathEl.setAttribute("data-name", name);

    svg.appendChild(pathEl);
    paths[name] = pathEl;

    pathEl.addEventListener("mousemove", (e) => {
      tooltip.style.display = "block";
      tooltip.textContent = name;
      const mapRect = mapDiv.getBoundingClientRect();
      let left = e.clientX - mapRect.left + 10;
      let top = e.clientY - mapRect.top + 10;

      if(left + tooltip.offsetWidth > mapRect.width) {
        left = e.clientX - mapRect.left - tooltip.offsetWidth - 8;
      }
      if(top + tooltip.offsetHeight > mapRect.height) {
        top = e.clientY - mapRect.top - tooltip.offsetHeight - 8;
      }

      tooltip.style.left = left + "px";
      tooltip.style.top = top + "px";

      clearHighlight();
      paths[name].classList.add("highlight");
    });

    pathEl.addEventListener("mouseleave", () => {
      tooltip.style.display = "none";
      clearHighlight();
    });

    pathEl.addEventListener("click", () => {
      selectMunicipio(name);
    });

    const legendItem = document.createElement("div");
    legendItem.textContent = name;
    legendItem.dataset.name = name;
    munList.appendChild(legendItem);

    legendItem.addEventListener("mouseenter", () => {
      clearHighlight();
      if(paths[name]) paths[name].classList.add("highlight");
    });
    legendItem.addEventListener("mouseleave", () => {
      clearHighlight();
    });
    legendItem.addEventListener("click", () => {
      selectMunicipio(name);
    });
  });
</script>

</body>
</html>
"""

components.html(html_code, height=500, scrolling=False)
