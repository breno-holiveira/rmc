import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregamento de dados
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

# Construir GeoJSON
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

gj = {"type": "FeatureCollection", "features": features}
geojson_js = json.dumps(gj)

# HTML/CSS/JS
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>RMC Interativo</title>
  <style>
    html, body {{
      height: 100%;
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(120deg, #f5f8fc, #e6ecf5);
      overflow: hidden;
    }}
    #sidebar {{
      position: fixed;
      top: 0;
      left: 0;
      width: 240px;
      height: 100vh;
      background: rgba(255, 255, 255, 0.82);
      backdrop-filter: blur(10px);
      border-right: 1px solid #c7d1e0;
      padding: 16px;
      overflow-y: auto;
      scroll-behavior: smooth;
      z-index: 10;
      box-shadow: 2px 0 8px rgba(0,0,0,0.06);
      transition: all 0.3s ease;
    }}
    #sidebar::-webkit-scrollbar {{
      width: 8px;
    }}
    #sidebar::-webkit-scrollbar-thumb {{
      background-color: rgba(140, 160, 190, 0.3);
      border-radius: 8px;
    }}
    #sidebar:hover::-webkit-scrollbar-thumb {{
      background-color: rgba(100, 130, 160, 0.5);
    }}
    #sidebar h2 {{
      margin: 0 0 12px;
      color: #2c3e70;
      font-size: 17px;
    }}
    #search {{
      width: 100%;
      padding: 8px;
      border-radius: 6px;
      border: 1px solid #ccd7e2;
      margin-bottom: 12px;
      background-color: #f9fbfd;
    }}
    #list div {{
      padding: 8px;
      border-radius: 6px;
      cursor: pointer;
      color: #2c3e70;
      transition: background 0.2s;
    }}
    #list div:hover {{
      background: rgba(180, 200, 230, 0.3);
    }}
    #list div.active {{
      background: #2c3e70;
      color: #fff;
      font-weight: 600;
    }}
    #map {{
      margin-left: 240px;
      height: 100vh;
      position: relative;
      overflow: hidden;
    }}
    svg {{
      width: 100%;
      height: 100%;
      display: block;
    }}
    .area {{
      fill: #c3d3e5;
      stroke: #415d84;
      stroke-width: 1;
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .area:hover {{
      fill: #9fb8d6;
      stroke-width: 1.4;
    }}
    .area.selected {{
      fill: #2c3e70;
    }}
    #tooltip {{
      position: fixed;
      background: rgba(44,62,112,0.95);
      color: white;
      padding: 6px 10px;
      font-size: 13px;
      border-radius: 5px;
      display: none;
      pointer-events: none;
      z-index: 1000;
    }}
    #info {{
      position: absolute;
      top: 24px;
      right: 24px;
      background: rgba(255,255,255,0.85);
      backdrop-filter: blur(12px);
      padding: 16px;
      border-radius: 10px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      max-width: 280px;
      font-size: 13px;
      display: none;
    }}
    #info.visible {{ display: block; }}
    #info h3 {{
      margin: 0 0 10px;
      color: #2c3e70;
    }}
    #info .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px 12px;
    }}
    #info .label {{
      font-weight: 600;
      color: #4d648d;
    }}
    #info .value {{
      text-align: right;
      color: #2d3f54;
    }}
    #info .fonte {{
      font-size: 10px;
      grid-column: 1/-1;
      color: #7a8ba3;
      margin-top: 10px;
      text-align: right;
    }}
  </style>
</head>
<body>
  <div id="sidebar">
    <h2>Municípios</h2>
    <input id="search" placeholder="Buscar..." />
    <div id="list"></div>
  </div>
  <div id="map">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg>
    <div id="tooltip"></div>
    <div id="info">
      <h3>Município</h3>
      <div class="grid">
        <div class="label">PIB 2021:</div><div class="value" id="pib"></div>
        <div class="label">% no PIB regional:</div><div class="value" id="part"></div>
        <div class="label">PIB per capita:</div><div class="value" id="percapita"></div>
        <div class="label">População:</div><div class="value" id="pop"></div>
        <div class="label">Área:</div><div class="value" id="area"></div>
        <div class="label">Densidade:</div><div class="value" id="dens"></div>
        <div class="fonte">Fonte: IBGE</div>
      </div>
    </div>
  </div>

  <script>
    const geo = {geojson_js};
    const svg = document.querySelector("svg");
    const tooltip = document.getElementById("tooltip");
    const info = document.getElementById("info");
    const list = document.getElementById("list");
    const search = document.getElementById("search");
    const paths = {{}};
    let selected = null;

    let coords = [];
    geo.features.forEach(f => {{
      const g = f.geometry;
      if (g.type === "Polygon") g.coordinates[0].forEach(c => coords.push(c));
      else if (g.type === "MultiPolygon") g.coordinates.forEach(p => p[0].forEach(c => coords.push(c)));
    }});
    const lons = coords.map(c => c[0]);
    const lats = coords.map(c => c[1]);
    const minX = Math.min(...lons), maxX = Math.max(...lons);
    const minY = Math.min(...lats), maxY = Math.max(...lats);

    function project([lon, lat]) {{
      const x = ((lon - minX) / (maxX - minX)) * 920 + 40;
      const y = 900 - ((lat - minY) / (maxY - minY)) * 880;
      return [x, y];
    }}
    function polygonToPath(coords) {{
      return coords.map(c => project(c).join(",")).join(" ");
    }}
    function select(name) {{
      if (selected) {{
        paths[selected].classList.remove("selected");
        [...list.children].forEach(d => d.classList.remove("active"));
      }}
      selected = name;
      if (paths[name]) {{
        paths[name].classList.add("selected");
        [...list.children].forEach(div => {{
          if (div.dataset.name === name) {{
            div.classList.add("active");
            div.scrollIntoView({{ behavior: "smooth", block: "center" }});
          }}
        }});
        showInfo(name);
      }}
    }}
    function showInfo(name) {{
      const f = geo.features.find(f => f.properties.name === name);
      if (!f) return;
      info.querySelector("h3").textContent = name;
      info.querySelector("#pib").textContent = f.properties.pib_2021 ? "R$ " + f.properties.pib_2021.toLocaleString("pt-BR") : "-";
      info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace('.', ',') + "%" : "-";
      info.querySelector("#percapita").textContent = f.properties.per_capita_2021 ? "R$ " + f.properties.per_capita_2021.toLocaleString("pt-BR") : "-";
      info.querySelector("#pop").textContent = f.properties.populacao_2022 ? f.properties.populacao_2022.toLocaleString("pt-BR") : "-";
      info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace(".", ",") + " km²" : "-";
      info.querySelector("#dens").textContent = f.properties.densidade_demografica_2022 ? f.properties.densidade_demografica_2022.toLocaleString("pt-BR") + " hab/km²" : "-";
      info.classList.add("visible");
    }}
    geo.features.forEach(f => {{
      const name = f.properties.name;
      let d = "";
      if (f.geometry.type === "Polygon") d = "M" + polygonToPath(f.geometry.coordinates[0]) + " Z";
      else if (f.geometry.type === "MultiPolygon") f.geometry.coordinates.forEach(p => d += "M" + polygonToPath(p[0]) + " Z ");
      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", d.trim());
      path.classList.add("area");
      path.setAttribute("data-name", name);
      svg.appendChild(path);
      paths[name] = path;

      path.addEventListener("mousemove", e => {{
        tooltip.style.left = (e.clientX + 10) + "px";
        tooltip.style.top = (e.clientY - 20) + "px";
        tooltip.textContent = name;
        tooltip.style.display = "block";
      }});
      path.addEventListener("mouseleave", () => tooltip.style.display = "none");
      path.addEventListener("click", () => select(name));

      const div = document.createElement("div");
      div.textContent = name;
      div.dataset.name = name;
      div.addEventListener("click", () => select(name));
      list.appendChild(div);
    }});
    search.addEventListener("input", e => {{
      const val = e.target.value.toLowerCase();
      [...list.children].forEach(d => {{
        d.style.display = d.textContent.toLowerCase().includes(val) ? "block" : "none";
      }});
    }});
    if (geo.features.length > 0) select(geo.features[0].properties.name);
  </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=650, scrolling=False)
