import streamlit as st
import geopandas as gpd
import json

st.set_page_config(layout="wide", page_title="RMC Data - Transparência", page_icon="📊")

st.title("RMC Data")
st.header("Dados e indicadores da Região Metropolitana de Campinas")

# Dados extras fixos (população, área, PIB)
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

@st.cache_data(show_spinner=True, allow_output_mutation=True)
def load_and_prepare_geojson():
    # Carrega shapefile e projeta para WGS84 se necessário
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values(by="NM_MUN")

    # Monta GeoJSON enriquecido com dados extras
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
    return geojson

geojson = load_and_prepare_geojson()
geojson_str = json.dumps(geojson)

# HTML + JS moderno + interativo (suave, minimalista, responsivo)
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC - Transparência</title>
<style>
  html, body {{
    margin: 0; padding: 0; height: 100vh;
    background: #fafafa;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    color: #222;
    user-select: none;
    display: flex;
    flex-direction: row;
    overflow: hidden;
  }}

  #legend {{
    width: 220px;
    background-color: #ffffffcc;
    padding: 15px 20px;
    box-sizing: border-box;
    overflow-y: auto;
    border-radius: 10px 0 0 10px;
    font-size: 13px;
    line-height: 1.3;
    color: #444;
    box-shadow: 1px 0 6px rgba(0,0,0,0.08);
    flex-shrink: 0;
  }}

  #legend strong {{
    font-size: 15px;
    color: #111;
    margin-bottom: 12px;
    display: block;
    font-weight: 700;
  }}

  #legend div {{
    padding: 7px 10px;
    margin-bottom: 6px;
    border-radius: 6px;
    cursor: pointer;
    color: #555;
    transition: background-color 0.25s ease, color 0.25s ease;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }}

  #legend div:hover {{
    background-color: #e8f0fe;
    color: #1a73e8;
  }}

  #legend div.active {{
    background-color: #1a73e8;
    color: white;
    font-weight: 700;
  }}

  #map {{
    flex-grow: 1;
    position: relative;
    background: #fff;
    border-radius: 0 10px 10px 0;
    min-width: 0;
    background-repeat: no-repeat;
    background-position: left, right;
    background-size: 40px 100%;
    box-shadow: inset 0 0 15px rgba(26, 115, 232, 0.08);
  }}

  svg {{
    width: 100%;
    height: 100vh;
    display: block;
    background: transparent;
  }}

  #info-panel {{
    position: absolute;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    width: 300px;
    background: #1a73e8ee;
    color: #fefefe;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 6px 20px rgba(26, 115, 232, 0.3);
    font-size: 14px;
    line-height: 1.5;
    user-select: text;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s ease;
  }}

  #info-panel.visible {{
    opacity: 1;
    pointer-events: auto;
  }}

  #info-panel h3 {{
    margin: 0 0 10px;
    font-weight: 700;
    font-size: 18px;
    color: #f1f1f1;
  }}

  #info-panel div {{
    margin-bottom: 8px;
  }}

  /* Scrollbars para legend e info */
  #legend::-webkit-scrollbar {{
    width: 6px;
  }}
  #legend::-webkit-scrollbar-track {{
    background: transparent;
  }}
  #legend::-webkit-scrollbar-thumb {{
    background-color: #a1a1a1;
    border-radius: 3px;
  }}
  #legend::-webkit-scrollbar-thumb:hover {{
    background-color: #7a7a7a;
  }}

  /* Polígonos */
  .polygon {{
    fill: rgba(26, 115, 232, 0.15);
    stroke: rgba(26, 115, 232, 0.6);
    stroke-width: 1;
    cursor: pointer;
    transition: stroke 0.25s ease, stroke-width 0.25s ease, fill 0.3s ease;
    opacity: 0.8;
  }}

  .polygon:hover {{
    fill: rgba(26, 115, 232, 0.3) !important;
    stroke-width: 2.5;
    filter: drop-shadow(0 0 7px rgba(26, 115, 232, 0.4));
    opacity: 1;
  }}

  .polygon.selected {{
    fill: rgba(26, 115, 232, 0.45);
    stroke: rgba(26, 115, 232, 0.9);
    stroke-width: 3;
    filter: drop-shadow(0 0 9px rgba(26, 115, 232, 0.5));
    opacity: 1;
  }}

  #tooltip {{
    position: absolute;
    pointer-events: none;
    padding: 6px 12px;
    background: #1a73e8dd;
    color: #fefefe;
    font-weight: 700;
    font-size: 12px;
    border-radius: 6px;
    white-space: nowrap;
    box-shadow: 0 0 10px rgba(26, 115, 232, 0.5);
    display: none;
    user-select: none;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }}
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
  <div id="info-panel" aria-live="polite" aria-label="Informações do município selecionado">
    <h3>Selecione um município</h3>
    <div><strong>População:</strong> –</div>
    <div><strong>Área:</strong> –</div>
    <div><strong>PIB (2021):</strong> –</div>
  </div>
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

  // Projeta coordenadas para SVG
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

  function formatNumber(num) {{
    if(num === null || num === undefined) return "N/A";
    return num.toLocaleString('pt-BR');
  }}

  function updateInfoPanel(data) {{
    if(!data) {{
      infoPanel.querySelector('h3').textContent = "Selecione um município";
      const divs = infoPanel.querySelectorAll('div');
      divs[0].innerHTML = "<strong>População:</strong> –";
      divs[1].innerHTML = "<strong>Área:</strong> –";
      divs[2].innerHTML = "<strong>PIB (2021):</strong> –";
      infoPanel.classList.remove("visible");
      return;
    }}
    infoPanel.querySelector('h3').textContent = data.name;
    const divs = infoPanel.querySelectorAll('div');
    divs[0].innerHTML = `<strong>População:</strong> ${{formatNumber(data.populacao)}}`;
    divs[1].innerHTML = `<strong>Área:</strong> ${{data.area ? data.area.toFixed(1) + " km²" : "N/A"}}`;
    divs[2].innerHTML = `<strong>PIB (2021):</strong> ${{data.pib_2021 ? "R$ " + formatNumber(data.pib_2021) : "N/A"}}`;
    infoPanel.classList.add("visible");
  }}

  function clearHighlight() {{
    Object.values(paths).forEach(p => p.classList.remove("highlight"));
  }}

  function clearSelection() {{
    Object.values(paths).forEach(p => p.classList.remove("selected"));
  }}

  function setActiveLegend(name) {{
    const legendItems = munList.children;
    for(let i=0; i < legendItems.length; i++) {{
      legendItems[i].classList.toggle("active", legendItems[i].dataset.name === name);
    }}
  }}

  function selectMunicipio(name) {{
    clearHighlight();
    clearSelection();
    if(paths[name]) paths[name].classList.add("selected");
    setActiveLegend(name);
    selectedName = name;

    // Atualiza painel de informações
    const data = geojson.features.find(f => f.properties.name === name);
    if (data) {{
      updateInfoPanel(data.properties);
    }}
  }}

  // Cria polígonos SVG e legenda interativa
  geojson.features.forEach(f => {{
    const props = f.properties;
    const name = props.name;
    const geom = f.geometry;
    let pathD = "";

    if (geom.type === "Polygon") {{
      const pathData = polygonToPath(geom.coordinates[0]);
      pathD = `M${{pathData}} Z`;
    }} else if (geom.type === "MultiPolygon") {{
      geom.coordinates.forEach(poly => {{
        const pathData = polygonToPath(poly[0]);
        pathD += `M${{pathData}} Z`;
      }});
    }}

    const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
    pathEl.setAttribute("d", pathD);
    pathEl.classList.add("polygon");
    pathEl.setAttribute("data-name", name);

    svg.appendChild(pathEl);
    paths[name] = pathEl;

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

    // Legenda interativa
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

# Renderiza no Streamlit com scroll e altura adequada
st.components.v1.html(html_code, height=720, scrolling=True)
