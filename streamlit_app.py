import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title='RMC Data',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown('# RMC Data')
st.markdown('### Indicadores da Região Metropolitana de Campinas')

# LOAD SHAPEFILE
gdf = gpd.read_file('./shapefile_rmc/RMC_municipios.shp')
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

# LOAD DADOS
df_dados = pd.read_excel('dados_rmc.xlsx')
df_dados.set_index("nome", inplace=True)

# CONSTRUIR GEOJSON COM PROPRIEDADES
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
            "densidade_demografica": dados["densidade_demografica_2022"]
        })

    features.append({"type": "Feature", "geometry": geom, "properties": props})

geojson = {"type": "FeatureCollection", "features": features}
geojson_safe = json.dumps(geojson).replace("'", "\\'")

# HTML EMBUTIDO
html_code = f"""
<iframe id="mapFrame" style="width:100%; height:700px; border:none;" srcdoc='
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <style>
    html, body {{
      margin: 0;
      height: 100%;
      font-family: "Segoe UI", Roboto, sans-serif;
      background: #f9fafc;
      color: #333;
      display: flex;
      flex-direction: row;
    }}
    #sidebar {{
      width: 240px;
      background: #ffffff;
      box-shadow: 2px 0 10px rgba(0,0,0,0.04);
      padding: 20px 16px;
      overflow-y: auto;
      border-right: 1px solid #e0e0e0;
    }}
    #sidebar h2 {{
      font-size: 17px;
      color: #0b3d91;
      margin-bottom: 16px;
      border-bottom: 1px solid #0b3d91;
      padding-bottom: 6px;
    }}
    #sidebar div {{
      margin: 6px 0;
      padding: 6px 10px;
      border-radius: 8px;
      transition: 0.3s;
      cursor: pointer;
      font-size: 14px;
    }}
    #sidebar div:hover {{
      background: #e6eef9;
      color: #0b3d91;
    }}
    #sidebar div.active {{
      background: #0b3d91;
      color: #fff;
      font-weight: bold;
    }}
    #map {{
      flex: 1;
      position: relative;
    }}
    svg {{
      width: 100%;
      height: 100%;
    }}
    .polygon {{
      fill: rgba(11, 61, 145, 0.15);
      stroke: rgba(11, 61, 145, 0.5);
      stroke-width: 1;
      transition: all 0.25s ease;
      cursor: pointer;
    }}
    .polygon:hover {{
      fill: rgba(11, 61, 145, 0.35);
      stroke-width: 2;
      filter: drop-shadow(0 0 6px rgba(11, 61, 145, 0.2));
    }}
    .polygon.selected {{
      fill: rgba(11, 61, 145, 0.45);
      stroke: rgba(11, 61, 145, 0.9);
      stroke-width: 2.5;
      filter: drop-shadow(0 0 10px rgba(11, 61, 145, 0.4));
    }}
    #info {{
      position: absolute;
      right: 20px;
      top: 20px;
      width: 320px;
      padding: 18px 22px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 4px 14px rgba(0,0,0,0.08);
      font-size: 14px;
      line-height: 1.6;
      display: none;
    }}
    #info.visible {{
      display: block;
    }}
    #info h3 {{
      margin-top: 0;
      font-size: 16px;
      color: #0b3d91;
    }}
    #info div strong {{
      color: #0b3d91;
    }}
    #info small {{
      display: block;
      margin-top: 16px;
      font-size: 11px;
      color: #999;
    }}
  </style>
</head>
<body>
  <div id="sidebar"><h2>Municípios</h2></div>
  <div id="map">
    <svg viewBox="0 0 1000 950"></svg>
    <div id="info"></div>
  </div>
<script>
const geo = JSON.parse('{geojson_safe}');
const svg = document.querySelector("svg");
const sidebar = document.getElementById("sidebar");
const info = document.getElementById("info");

let selected = null;

// Projeção simplificada
const bounds = geo.features.flatMap(f => {{
  const coords = f.geometry.type === "Polygon"
    ? f.geometry.coordinates[0]
    : f.geometry.coordinates.flat(2);
  return coords;
}});
const lons = bounds.map(p => p[0]);
const lats = bounds.map(p => p[1]);
const minX = Math.min(...lons), maxX = Math.max(...lons);
const minY = Math.min(...lats), maxY = Math.max(...lats);
const scaleX = 950 / (maxX - minX);
const scaleY = 900 / (maxY - minY);
function project(x, y) {{
  return [(x - minX) * scaleX + 20, (maxY - y) * scaleY + 20];
}}

// Criar paths SVG
geo.features.forEach(f => {{
  let d = "";
  const coords = f.geometry.type === "Polygon"
    ? [f.geometry.coordinates]
    : f.geometry.coordinates;
  coords.forEach(poly => {{
    poly.forEach(ring => {{
      ring.forEach((pt, i) => {{
        const [x, y] = project(pt[0], pt[1]);
        d += (i === 0 ? "M" : "L") + x.toFixed(1) + "," + y.toFixed(1);
      }});
      d += "Z ";
    }});
  }});
  const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("d", d.trim());
  path.classList.add("polygon");
  path.dataset.name = f.properties.name;
  path.addEventListener("click", () => selectMunicipio(f));
  svg.appendChild(path);

  // Sidebar
  const item = document.createElement("div");
  item.textContent = f.properties.name;
  item.dataset.name = f.properties.name;
  item.addEventListener("click", () => selectMunicipio(f));
  sidebar.appendChild(item);
}});

function formatBR(val, prefix='') {{
  if (val === null || val === undefined) return "-";
  return prefix + parseFloat(val).toLocaleString("pt-BR");
}}

function selectMunicipio(f) {{
  document.querySelectorAll(".polygon").forEach(p => p.classList.remove("selected"));
  document.querySelectorAll("#sidebar div").forEach(d => d.classList.remove("active"));
const sel = svg.querySelector(`[data-name="${{f.properties.name}}"]`);
const div = sidebar.querySelector(`[data-name="${{f.properties.name}}"]`);
  if (sel) sel.classList.add("selected");
  if (div) div.classList.add("active");

  const p = f.properties;
  info.innerHTML = `
    <h3>${{p.name}}</h3>
    <div><strong>PIB (2021):</strong> R$ ${{formatBR(p.pib_2021)}}</div>
    <div><strong>Participação RMC:</strong> ${{(p.participacao_rmc * 100).toFixed(2).replace('.', ',')}}%</div>
    <div><strong>PIB per capita:</strong> R$ ${{formatBR(p.pib_per_capita)}}</div>
    <div><strong>População:</strong> ${{formatBR(p.populacao)}}</div>
    <div><strong>Área:</strong> ${{p.area.toFixed(1).replace('.', ',')}} km²</div>
    <div><strong>Densidade demográfica:</strong> ${{formatBR(p.densidade_demografica)}} hab/km²</div>
    <small>Fonte: IBGE Cidades</small>
  `;
  info.classList.add("visible");
}
</script>
</body>
</html>'>
</iframe>
"""

st.components.v1.html(html_code, height=720, scrolling=False)
