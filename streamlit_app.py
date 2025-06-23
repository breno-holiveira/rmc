import streamlit as st
import geopandas as gpd
import json

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("RMC Data")
st.header("Dados e indicadores da Região Metropolitana de Campinas")

# Dados extras dos municípios
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

@st.cache_data(show_spinner=True)
def load_geojson():
    # Carrega shapefile e projeta para EPSG:4326
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values("NM_MUN")

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
                "pib_2021": extra["pib_2021"],
            },
            "geometry": geom,
        })
    return {"type": "FeatureCollection", "features": features}

geojson = load_geojson()
geojson_str = json.dumps(geojson)

# HTML + CSS + JS para o mapa interativo minimalista e profissional
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC</title>
<style>
  /* Reset básico */
  * {{
    margin: 0; padding: 0; box-sizing: border-box;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  }}
  body, html {{
    width: 100vw; height: 100vh;
    background: #f8f9fa;
    color: #212529;
    display: flex;
    overflow: hidden;
  }}
  #legend {{
    width: 240px;
    background: #ffffffcc;
    border-right: 1px solid #ddd;
    padding: 1rem;
    overflow-y: auto;
  }}
  #legend strong {{
    display: block;
    margin-bottom: 1rem;
    font-weight: 700;
    color: #0d6efd;
  }}
  #legend div {{
    padding: 6px 10px;
    border-radius: 5px;
    margin-bottom: 6px;
    cursor: pointer;
    user-select: none;
    transition: background-color 0.3s ease, color 0.3s ease;
    color: #495057;
    font-size: 0.9rem;
  }}
  #legend div:hover {{
    background-color: #e7f1ff;
    color: #0d6efd;
  }}
  #legend div.active {{
    background-color: #0d6efd;
    color: #fff;
    font-weight: 600;
  }}

  #map-container {{
    flex-grow: 1;
    position: relative;
    background: #ffffff;
  }}

  svg {{
    width: 100%;
    height: 100vh;
    display: block;
  }}

  .polygon {{
    fill: rgba(13, 110, 253, 0.15);
    stroke: rgba(13, 110, 253, 0.6);
    stroke-width: 1;
    cursor: pointer;
    transition: all 0.3s ease;
    opacity: 0.8;
  }}
  .polygon:hover {{
    fill: rgba(13, 110, 253, 0.3);
    stroke-width: 2;
    filter: drop-shadow(0 0 5px rgba(13,110,253,0.4));
    opacity: 1;
  }}
  .polygon.selected {{
    fill: rgba(13, 110, 253, 0.5);
    stroke-width: 3;
    filter: drop-shadow(0 0 8px rgba(13,110,253,0.7));
    opacity: 1;
  }}

  #info-panel {{
    width: 300px;
    background: #fff;
    border-left: 1px solid #ddd;
    padding: 1rem 1.5rem;
    font-size: 0.9rem;
    overflow-y: auto;
  }}
  #info-panel h3 {{
    margin-bottom: 1rem;
    color: #0d6efd;
  }}
  #info-panel div {{
    margin-bottom: 0.7rem;
  }}

  #tooltip {{
    position: absolute;
    pointer-events: none;
    background: rgba(13, 110, 253, 0.85);
    color: #fff;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.8rem;
    user-select: none;
    display: none;
    box-shadow: 0 0 8px rgba(13, 110, 253, 0.7);
    white-space: nowrap;
    z-index: 10;
  }}
</style>
</head>
<body>

<div id="legend" role="list" aria-label="Lista de municípios da Região Metropolitana de Campinas">
  <strong>Selecione um município</strong>
  <div id="mun-list"></div>
</div>

<div id="map-container" role="region" aria-label="Mapa interativo dos municípios da RMC">
  <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"></svg>
  <div id="tooltip" role="tooltip"></div>
</div>

<div id="info-panel" role="region" aria-live="polite" aria-label="Informações do município selecionado">
  <h3>Selecione um município</h3>
  <div><strong>População:</strong> –</div>
  <div><strong>Área:</strong> –</div>
  <div><strong>PIB (2021):</strong> –</div>
</div>

<script>
  const geojson = {geojson_str};
  const svg = document.querySelector("svg");
  const munList = document.getElementById("mun-list");
  const tooltip = document.getElementById("tooltip");
  const infoPanel = document.getElementById("info-panel");
  const mapContainer = document.getElementById("map-container");

  let selectedName = null;
  const paths = {{}};

  // Obter todas as coordenadas para calcular escala e projeção simples
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

  // Projeção simples linear para SVG
  function project(coord) {{
    const [lon, lat] = coord;
    const x = ((lon - minLon) / (maxLon - minLon)) * 900 + 50;
    const y = 900 - ((lat - minLat) / (maxLat - minLat)) * 850;
    return [x, y];
  }}

  // Converte coordenadas do polígono para atributo 'd' do <path>
  function polygonToPath(coords) {{
    return coords.map(c => {{
      const [x, y] = project(c);
      return x + "," + y;
    }}).join(" ");
  }}

  // Formata números para BR locale com separadores de milhar
  function formatNumber(num) {{
    if(num === null || num === undefined) return "N/A";
    return num.toLocaleString('pt-BR');
  }}

  // Atualiza painel de informações do município selecionado
  function updateInfoPanel(data) {{
    if(!data) {{
      infoPanel.querySelector('h3').textContent = "Selecione um município";
      let divs = infoPanel.querySelectorAll('div');
      divs[0].innerHTML = "<strong>População:</strong> –";
      divs[1].innerHTML = "<strong>Área:</strong> –";
      divs[2].innerHTML = "<strong>PIB (2021):</strong> –";
      return;
    }}
    infoPanel.querySelector('h3').textContent = data.name;
    infoPanel.querySelectorAll('div')[0].innerHTML = `<strong>População:</strong> ${formatNumber(data.populacao)}`;
    infoPanel.querySelectorAll('div')[1].innerHTML = `<strong>Área:</strong> ${data.area ? data.area.toFixed(1) + " km²" : "N/A"}`;
    infoPanel.querySelectorAll('div')[2].innerHTML = `<strong>PIB (2021):</strong> ${data.pib_2021 ? "R$ " + formatNumber(data.pib_2021) : "N/A"}`;
  }}

  // Limpa todos os highlights (hover)
  function clearHighlight() {{
    Object.values(paths).forEach(p => p.classList.remove("highlight"));
  }}

  // Limpa todas as seleções
  function clearSelection() {{
    Object.values(paths).forEach(p => p.classList.remove("selected"));
  }}

  // Atualiza legenda com o item ativo selecionado
  function setActiveLegend(name) {{
    const legendItems = munList.children;
    for(let i=0; i < legendItems.length; i++) {{
      legendItems[i].classList.toggle("active", legendItems[i].dataset.name === name);
    }}
  }}

  // Função principal para selecionar município
  function selectMunicipio(name) {{
    clearHighlight();
    clearSelection();
    if(paths[name]) paths[name].classList.add("selected");
    setActiveLegend(name);
    selectedName = name;

    const data = geojson.features.find(f => f.properties.name === name);
    if(data) updateInfoPanel(data.properties);
  }}

  // Cria os paths SVG para cada município, e itens da legenda
  geojson.features.forEach(f => {{
    const props = f.properties;
    const name = props.name;
    const geom = f.geometry;
    let pathD = "";

    if(geom.type === "Polygon") {{
      pathD = `M${polygonToPath(geom.coordinates[0])} Z`;
    }} else if(geom.type === "MultiPolygon") {{
      geom.coordinates.forEach(poly => {{
        pathD += `M${polygonToPath(poly[0])} Z`;
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

      const mapRect = mapContainer.getBoundingClientRect();
      let left = e.clientX - mapRect.left + 12;
      let top = e.clientY - mapRect.top + 12;

      if(left + tooltip.offsetWidth > mapRect.width) {{
        left = e.clientX - mapRect.left - tooltip.offsetWidth - 12;
      }}
      if(top + tooltip.offsetHeight > mapRect.height) {{
        top = e.clientY - mapRect.top - tooltip.offsetHeight - 12;
      }}

      tooltip.style.left = left + "px";
      tooltip.style.top = top + "px";

      clearHighlight();
      if(!pathEl.classList.contains("selected")) {{
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

    // Legenda
    const legendItem = document.createElement("div");
    legendItem.textContent = name;
    legendItem.dataset.name = name;
    munList.appendChild(legendItem);

    legendItem.addEventListener("mouseenter", () => {{
      clearHighlight();
      if(paths[name] && !paths[name].classList.contains("selected")) {{
        paths[name].classList.add("highlight");
      }}
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

st.components.v1.html(html_code, height=720, scrolling=True)
