import streamlit as st
import geopandas as gpd
import json
import streamlit.components.v1 as components

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
  html, body {{
    margin: 0; padding: 0;
    height: 100%;
    background-color: #121212;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    color: #ddd;
    user-select: none;
    display: flex;
  }}

  #legend {{
    width: 180px;
    background-color: rgba(18, 18, 18, 0.85);
    padding: 14px 16px;
    box-sizing: border-box;
    overflow-y: auto;
    border-radius: 10px 0 0 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.7);
    font-size: 13px;
    line-height: 1.3;
    color: #bbb;
  }}

  #legend strong {{
    font-size: 16px;
    color: #eee;
    margin-bottom: 12px;
    display: block;
    font-weight: 600;
  }}

  #legend div {{
    padding: 6px 10px;
    margin-bottom: 5px;
    border-radius: 5px;
    cursor: pointer;
    color: #999;
    transition: background-color 0.3s ease, color 0.3s ease;
  }}
  #legend div:hover {{
    background-color: #224466;
    color: #a0c4ff;
    font-weight: 600;
  }}
  #legend div.active {{
    background-color: #335a99;
    color: #cbd8ff;
    font-weight: 700;
    box-shadow: 0 0 6px #335a99aa;
  }}

  #map {{
    flex: 2.2;
    position: relative;
    background: linear-gradient(135deg, #1a1a1a, #0f0f0f);
    border-radius: 0 10px 10px 0;
    box-shadow: inset 0 0 18px #000c;
  }}

  svg {{
    width: 100%;
    height: 100%;
    display: block;
    background: transparent;
  }}

  .polygon {{
    fill: rgba(80, 150, 255, 0.14);
    stroke: #444444;
    stroke-width: 1.3;
    opacity: 0.85;
    cursor: pointer;
    transition: stroke 0.3s ease, stroke-width 0.3s ease, opacity 0.3s ease, fill 0.3s ease;
  }}
  .polygon.highlight {{
    stroke: #5599ff !important;
    stroke-width: 2.6 !important;
    opacity: 1 !important;
  }}

  #tooltip {{
    position: absolute;
    pointer-events: none;
    padding: 2px 6px;
    background: rgba(85, 153, 255, 0.9);
    color: #121212;
    font-weight: 500;
    font-size: 11px;
    border-radius: 4px;
    white-space: nowrap;
    box-shadow: 0 0 6px rgba(85, 153, 255, 0.4);
    display: none;
    user-select: none;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }}

  #info-panel {{
    position: absolute;
    top: 12px;
    right: 12px;
    width: 180px;
    background: rgba(18, 18, 18, 0.68);
    border-radius: 8px;
    box-shadow: 0 0 14px rgba(85, 153, 255, 0.65);
    padding: 6px 10px;
    font-size: 11px;
    color: #bbb;
    user-select: none;
    display: none;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  }}
  #info-panel h3 {{
    margin-top: 0;
    font-weight: 700;
    font-size: 13px;
    color: #7eb2ff;
    border-bottom: 1.5px solid #5599ff;
    padding-bottom: 3px;
  }}
  #info-panel div {{
    margin-bottom: 5px;
  }}

  /* Scrollbar legenda */
  #legend::-webkit-scrollbar {{
    width: 6px;
  }}
  #legend::-webkit-scrollbar-track {{
    background: transparent;
  }}
  #legend::-webkit-scrollbar-thumb {{
    background-color: #333;
    border-radius: 3px;
  }}
  #legend::-webkit-scrollbar-thumb:hover {{
    background-color: #555;
  }}
</style>
</head>
<body>

<div id="legend" role="list" aria-label="Lista de municípios da Região Metropolitana de Campinas">
  <strong>Municípios RMC</strong>
  <div id="mun-list"></div>
</div>

<div id="map" role="region" aria-label="Mapa interativo dos municípios da RMC">
  <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"></svg>
  <div id="tooltip" role="tooltip"></div>
  <div id="info-panel" aria-live="polite"></div>
</div>

<script>
  const geojson = {geojson_str};
  const svg = document.querySelector("svg");
  const munList = document.getElementById("mun-list");
  const tooltip = document.getElementById("tooltip");
  const mapDiv = document.getElementById("map");
  const infoPanel = document.getElementById("info-panel");

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

  const paths = {{}};

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

  function showInfo(data) {{
    if(!data) {{
      infoPanel.style.display = "none";
      return;
    }}
    const pop = formatNumber(data.populacao);
    const area = data.area ? data.area.toFixed(1) + " km²" : "N/A";
    const pib = data.pib_2021 ? "R$ " + formatNumber(data.pib_2021) : "N/A";

    infoPanel.innerHTML = `
      <h3>${{data.name}}</h3>
      <div><strong>População:</strong> ${{pop}}</div>
      <div><strong>Área:</strong> ${{area}}</div>
      <div><strong>PIB (2021):</strong> ${{pib}}</div>
    `;
    infoPanel.style.display = "block";
  }}

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
        top = e.clientY - mapDiv.getBoundingClientRect().top - tooltip.offsetHeight - 8;
      }}

      tooltip.style.left = left + "px";
      tooltip.style.top = top + "px";

      // Apenas o município em foco é destacado
      clearHighlight();
      paths[name].classList.add("highlight");
    }});

    pathEl.addEventListener("mouseleave", () => {{
      tooltip.style.display = "none";
      clearHighlight();
    }});

    pathEl.addEventListener("click", () => {{
      showInfo(props);
      setActiveLegend(name);
    }});

    const legendItem = document.createElement("div");
    legendItem.textContent = name;
    legendItem.dataset.name = name;
    munList.appendChild(legendItem);

    legendItem.addEventListener("mouseenter", () => {{
      clearHighlight();
      if(paths[name]) paths[name].classList.add("highlight");
    }});
    legendItem.addEventListener("mouseleave", () => {{
      clearHighlight();
    }});

    legendItem.addEventListener("click", () => {{
      showInfo(props);
      setActiveLegend(name);
    }});
  }});

  function clearHighlight() {{
    Object.values(paths).forEach(p => p.classList.remove("highlight"));
  }}

  function setActiveLegend(name) {{
    const legendItems = munList.children;
    for(let i=0; i < legendItems.length; i++) {{
      legendItems[i].classList.toggle("active", legendItems[i].dataset.name === name);
    }}
  }}
</script>

</body>
</html>
"""

components.html(html_code, height=650, scrolling=False)
