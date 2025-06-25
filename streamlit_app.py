import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")

st.title("RMC bData")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

# Carregamento dos dados
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

with open("grafico.html", "w", encoding="utf-8") as f:
    f.write(f"""
<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
<meta charset=\"UTF-8\" />
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
<title>Mapa Interativo RMC</title>
<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css\">
<style>
  html, body {{ margin: 0; padding: 0; height: 100vh; overflow: hidden; font-family: 'Segoe UI', sans-serif; }}
  #sidebar {{ width: 250px; background: #fff; border-right: 1px solid #ccc; padding: 10px; float: left; height: 100vh; overflow-y: auto; }}
  #map {{ position: relative; height: 100vh; width: calc(100% - 250px); float: left; }}
  svg {{ width: 100%; height: 100%; }}
  .area {{ fill: #b6cce5; stroke: #4d648d; stroke-width: 1; cursor: pointer; }}
  .area:hover {{ fill: #8db3dd; }}
  .area.selected {{ fill: #4d648d; stroke: #1a2d5a; }}
  #tooltip {{ position: absolute; background: #333; color: #fff; padding: 5px 10px; font-size: 12px; border-radius: 4px; display: none; pointer-events: none; z-index: 10; }}
  #info {{ position: fixed; bottom: 20px; right: 20px; width: 320px; max-height: 400px; background: rgba(255,255,255,0.9); border-radius: 16px; padding: 20px; box-shadow: 0 4px 16px rgba(0,0,0,0.2); display: none; overflow-y: auto; backdrop-filter: blur(6px); }}
  #info.visible {{ display: block; animation: fadeInUp 0.4s ease-out; }}
  @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  #info h3 {{ margin-top: 0; font-size: 18px; color: #1a2d5a; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .label {{ font-weight: bold; color: #4d648d; }}
  .value {{ text-align: right; color: #2c3e70; }}
  .fonte {{ grid-column: 1 / -1; font-size: 10px; color: #7f8caa; text-align: right; font-style: italic; }}
</style>
</head>
<body>
<div id=\"sidebar\"><h3>Municípios</h3><input type=\"text\" id=\"search\" placeholder=\"Buscar...\"><div id=\"list\"></div></div>
<div id=\"map\"><svg viewBox=\"0 0 1000 950\"></svg><div id=\"tooltip\"></div></div>
<div id=\"info\"><h3>Município</h3><div class=\"grid\"><div class=\"label\">PIB:</div><div class=\"value\" id=\"pib\"></div><div class=\"label\">% PIB RMC:</div><div class=\"value\" id=\"part\"></div><div class=\"label\">Per capita:</div><div class=\"value\" id=\"percapita\"></div><div class=\"label\">População:</div><div class=\"value\" id=\"pop\"></div><div class=\"label\">Área:</div><div class=\"value\" id=\"area\"></div><div class=\"label\">Densidade:</div><div class=\"value\" id=\"dens\"></div><div class=\"fonte\">Fonte: IBGE Cidades</div></div></div>
<script>
const geo = {geojson_str};
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
  else g.coordinates.forEach(p => p[0].forEach(c => coords.push(c)));
}});
const lons = coords.map(c => c[0]), lats = coords.map(c => c[1]);
const minX = Math.min(...lons), maxX = Math.max(...lons);
const minY = Math.min(...lats), maxY = Math.max(...lats);
function project([lon, lat]) {{
  const x = ((lon - minX) / (maxX - minX)) * 920 + 40;
  const y = 900 - ((lat - minY) / (maxY - minY)) * 880;
  return [x, y];
}}
function polygonToPath(coords) {{ return coords.map(c => project(c).join(",")).join(" "); }}
function select(name) {{
  if (selected) {{ paths[selected].classList.remove("selected"); }}
  selected = name;
  if (paths[name]) {{ paths[name].classList.add("selected"); showInfo(name); }}
}}
function showInfo(name) {{
  const f = geo.features.find(f => f.properties.name === name);
  if (!f) return;
  info.classList.add("visible");
  info.querySelector("#pib").textContent = f.properties.pib_2021 ? "R$ " + f.properties.pib_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#part").textContent = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2).replace('.', ',') + "%" : "-";
  info.querySelector("#percapita").textContent = f.properties.per_capita_2021 ? "R$ " + f.properties.per_capita_2021.toLocaleString("pt-BR") : "-";
  info.querySelector("#pop").textContent = f.properties.populacao_2022 ? f.properties.populacao_2022.toLocaleString("pt-BR") : "-";
  info.querySelector("#area").textContent = f.properties.area ? f.properties.area.toFixed(2).replace('.', ',') + " km²" : "-";
  info.querySelector("#dens").textContent = f.properties.densidade_demografica_2022 ? f.properties.densidade_demografica_2022.toLocaleString("pt-BR") + " hab/km²" : "-";
}}
geo.features.forEach(f => {{
  const name = f.properties.name;
  let d = "";
  if (f.geometry.type === "Polygon") d = "M" + polygonToPath(f.geometry.coordinates[0]) + " Z";
  else f.geometry.coordinates.forEach(p => {{ d += "M" + polygonToPath(p[0]) + " Z "; }});
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", d.trim());
  path.classList.add("area");
  path.setAttribute("data-name", name);
  svg.appendChild(path);
  paths[name] = path;
  path.addEventListener("mousemove", e => {{ tooltip.style.left = e.clientX + 10 + "px"; tooltip.style.top = e.clientY - 20 + "px"; tooltip.textContent = name; tooltip.style.display = "block"; }});
  path.addEventListener("mouseleave", () => tooltip.style.display = "none");
  path.addEventListener("click", () => select(name));
  const div = document.createElement("div");
  div.textContent = name;
  div.dataset.name = name;
  div.addEventListener("click", () => select(name));
  list.appendChild(div);
}});
search.addEventListener("input", e => {
  const val = e.target.value.toLowerCase();
  [...list.children].forEach(d => { d.style.display = d.textContent.toLowerCase().includes(val) ? "block" : "none"; });
});
if (geo.features.length > 0) select(geo.features[0].properties.name);
</script>
</body>
</html>
""")

# Exibe o HTML no Streamlit
with open("grafico.html", "r", encoding="utf-8") as f:
    st.components.v1.html(f.read(), height=750, scrolling=False)
