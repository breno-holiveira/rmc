import streamlit as st
import geopandas as gpd
import json
from pathlib import Path

st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="collapsed")
st.title("RMC Data")
st.header("Dados e indicadores da Região Metropolitana de Campinas")

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
gdf = gdf.to_crs("EPSG:4326") if gdf.crs != "EPSG:4326" else gdf
gdf = gdf.sort_values(by="NM_MUN")

features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    props = dados_extra.get(nome, {})
    features.append({
        "type": "Feature",
        "properties": {
            "name": nome,
            "populacao": props.get("populacao"),
            "area": props.get("area"),
            "pib_2021": props.get("pib_2021")
        },
        "geometry": row["geometry"].__geo_interface__
    })

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

with open("mapa_rmc_simplificado.html", "w", encoding="utf-8") as f:
    f.write(f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC</title>
<style>
  html, body {{ margin: 0; height: 100%; font-family: sans-serif; background: #fff; display: flex; }}
  #legend {{ width: 210px; padding: 16px; background: #fff; border-right: 1px solid #ccc; overflow-y: auto; }}
  #legend strong {{ display: block; font-size: 15px; margin-bottom: 12px; color: #0b3d91; }}
  #legend div {{ padding: 8px; cursor: pointer; font-size: 14px; border-radius: 4px; transition: 0.2s; }}
  #legend div:hover:not(.active) {{ background: #eef4ff; color: #0b3d91; }}
  #legend div.active {{ background: #0b3d91; color: white; font-weight: bold; }}
  #map {{ flex: 1; position: relative; }}
  svg {{ width: 100%; height: 100vh; display: block; }}
  #info-panel {{ width: 260px; padding: 16px; background: #f9f9f9; border-left: 1px solid #ccc; font-size: 14px; }}
  #info-panel h3 {{ margin: 0 0 10px; font-size: 16px; color: #0b3d91; }}
  #info-panel div strong {{ display: inline-block; width: 100px; color: #0b3d91; }}
  .polygon {{ fill: rgba(11,61,145,0.15); stroke: rgba(11,61,145,0.6); stroke-width: 1; cursor: pointer; }}
  .polygon:hover {{ fill: rgba(11,61,145,0.3); stroke-width: 2; }}
  .polygon.selected {{ fill: rgba(11,61,145,0.45); stroke-width: 2.5; }}
</style>
</head>
<body>
<nav id="legend"><strong>Municípios</strong><div id="mun-list"></div></nav>
<main id="map"><svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet"></svg></main>
<aside id="info-panel"><h3>Selecione um município</h3>
<div><strong>População:</strong> <span>-</span></div>
<div><strong>Área:</strong> <span>-</span></div>
<div><strong>PIB (2021):</strong> <span>-</span></div></aside>
<script>
const geojson = {geojson_str};
const svg = document.querySelector("svg");
const munList = document.getElementById("mun-list");
const infoPanel = document.getElementById("info-panel");
let selectedName = null, paths = {{}};

let coords = [];
geojson.features.forEach(f => {{
  const g = f.geometry;
  (g.type === "Polygon" ? [g.coordinates] : g.coordinates).forEach(poly => 
    poly[0].forEach(c => coords.push(c)));
}});
const [minLon, maxLon] = [Math.min(...coords.map(c => c[0])), Math.max(...coords.map(c => c[0]))];
const [minLat, maxLat] = [Math.min(...coords.map(c => c[1])), Math.max(...coords.map(c => c[1]))];

function project([lon, lat]) {{
  const x = ((lon - minLon) / (maxLon - minLon)) * 900 + 50;
  const y = 900 - ((lat - minLat) / (maxLat - minLat)) * 850;
  return [x, y];
}}
function polyPath(coords) {{ return coords.map(c => project(c).join(",")).join(" "); }}
function format(num) {{ return num?.toLocaleString("pt-BR") ?? "N/A"; }}
function updateInfo(d) {{
  infoPanel.querySelector("h3").textContent = d?.name || "Selecione um município";
  const [p, a, pib] = infoPanel.querySelectorAll("span");
  p.textContent = format(d?.populacao); a.textContent = d?.area ? d.area.toFixed(1)+" km²" : "N/A";
  pib.textContent = d?.pib_2021 ? "R$ " + format(d.pib_2021) : "N/A";
}}
function select(name) {{
  Object.values(paths).forEach(p => p.classList.remove("selected"));
  if(paths[name]) paths[name].classList.add("selected");
  Array.from(munList.children).forEach(div => div.classList.toggle("active", div.dataset.name === name));
  selectedName = name;
  updateInfo(geojson.features.find(f => f.properties.name === name)?.properties);
}}
geojson.features.forEach(f => {{
  const n = f.properties.name;
  let d = "";
  if(f.geometry.type === "Polygon") {{
    d = "M" + polyPath(f.geometry.coordinates[0]) + " Z";
  }} else {{
    f.geometry.coordinates.forEach(p => d += "M" + polyPath(p[0]) + " Z");
  }}
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", d);
  path.classList.add("polygon");
  svg.appendChild(path);
  paths[n] = path;
  path.addEventListener("click", () => select(n));

  const div = document.createElement("div");
  div.textContent = n; div.dataset.name = n;
  div.onclick = () => select(n);
  munList.appendChild(div);
}});
</script>
</body>
</html>
""")

# Renderiza no Streamlit
st.components.v1.html(Path("mapa_rmc_simplificado.html").read_text(encoding="utf-8"), height=620, scrolling=False)
