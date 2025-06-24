import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(
    page_title='RMC Data',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='collapsed'
)

st.markdown("""
    <style>
    /* Ajustes globais para suavidade */
    html, body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f7fa;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    iframe {
        border: none !important;
        border-radius: 12px;
        box-shadow: 0 0 12px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("RMC Data – Transparência Municipal")
st.markdown("""
<div style='font-size:18px; color:#333;'>
    Explore os principais indicadores socioeconômicos dos municípios da Região Metropolitana de Campinas. Clique no mapa ou na legenda para interagir.
</div>
""", unsafe_allow_html=True)

# SHAPEFILE
shapefile_path = './shapefile_rmc/RMC_municipios.shp'
gdf = gpd.read_file(shapefile_path)
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

# DADOS COMPLEMENTARES
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
            "pib_2021": dados.get("pib_2021"),
            "participacao_rmc": dados.get("participacao_rmc"),
            "pib_per_capita": dados.get("per_capita_2021"),
            "populacao": dados.get("populacao_2022"),
            "area": dados.get("area"),
            "densidade_demografica": dados.get("densidade_demografica_2022")
        })

    features.append({
        "type": "Feature",
        "geometry": geom,
        "properties": props
    })

geojson = {"type": "FeatureCollection", "features": features}
geojson_serialized = json.dumps(geojson).replace('{', '{{').replace('}', '}}')

# HTML FINAL COM JS E DESIGN SUAVE
html_code = f"""
<iframe srcdoc="""
<!DOCTYPE html>
<html lang='pt-BR'>
<head>
<meta charset='UTF-8'>
<title>Mapa Interativo RMC</title>
<style>
  html, body {{
    margin: 0;
    padding: 0;
    height: 100vh;
    font-family: 'Segoe UI', sans-serif;
    background-color: #f5f7fa;
  }}
  .container {{
    display: flex;
    height: 100%;
  }}
  #legend {{
    width: 260px;
    padding: 1rem;
    background: #ffffff;
    overflow-y: auto;
    border-right: 1px solid #ddd;
    box-shadow: 2px 0 5px rgba(0,0,0,0.05);
  }}
  #map-area {{
    flex-grow: 1;
    position: relative;
    background: #ffffff;
  }}
  svg {{
    width: 100%;
    height: 100%;
  }}
  .polygon {{
    fill: rgba(11,61,145,0.1);
    stroke: rgba(11,61,145,0.6);
    stroke-width: 1;
    transition: all 0.3s ease;
    cursor: pointer;
  }}
  .polygon:hover {{
    fill: rgba(11,61,145,0.2);
    stroke-width: 2;
    filter: drop-shadow(0 0 4px rgba(11,61,145,0.2));
  }}
  .selected {{
    fill: rgba(11,61,145,0.4);
    stroke-width: 2.5;
  }}
  #info-panel {{
    position: absolute;
    right: 20px;
    top: 20px;
    width: 300px;
    background: #fff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0,0,0,0.08);
    font-size: 14px;
    color: #333;
    display: none;
  }}
  #info-panel h3 {{
    margin-top: 0;
    font-size: 16px;
    color: #0b3d91;
    margin-bottom: 10px;
  }}
  #info-panel div {{
    margin-bottom: 8px;
  }}
  #info-panel small {{
    display: block;
    margin-top: 1rem;
    font-size: 11px;
    color: #777;
    text-align: right;
  }}
</style>
</head>
<body>
<div class='container'>
  <div id='legend'></div>
  <div id='map-area'>
    <svg viewBox='0 0 1000 900'></svg>
    <div id='info-panel'>
      <h3>Município</h3>
      <div><strong>PIB:</strong> <span id='pib'></span></div>
      <div><strong>Participação:</strong> <span id='part'></span></div>
      <div><strong>Per capita:</strong> <span id='percapita'></span></div>
      <div><strong>População:</strong> <span id='pop'></span></div>
      <div><strong>Área:</strong> <span id='area'></span></div>
      <div><strong>Densidade:</strong> <span id='dens'></span></div>
      <small>Fonte: IBGE Cidades</small>
    </div>
  </div>
</div>
<script>
const geojson = JSON.parse(`{geojson_serialized}`);
const svg = document.querySelector('svg');
const legend = document.getElementById('legend');
const info = document.getElementById('info-panel');

let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
geojson.features.forEach(f => {
  const coords = f.geometry.coordinates.flat(2);
  coords.forEach(([x, y]) => {
    minX = Math.min(minX, x);
    minY = Math.min(minY, y);
    maxX = Math.max(maxX, x);
    maxY = Math.max(maxY, y);
  });
});
const scaleX = 900 / (maxX - minX);
const scaleY = 850 / (maxY - minY);
const proj = ([x, y]) => [((x - minX) * scaleX + 50), (850 - (y - minY) * scaleY + 25)];

geojson.features.forEach(f => {
  const name = f.properties.name;
  const g = f.geometry;
  let path = "";
  const makePath = (poly) => poly.map((c, i) => {
    const [x, y] = proj(c);
    return `${i ? 'L' : 'M'}${x},${y}`;
  }).join(' ') + "Z";

  if (g.type === "Polygon") {
    path = makePath(g.coordinates[0]);
  } else {
    g.coordinates.forEach(ring => path += makePath(ring[0]));
  }

  const el = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  el.setAttribute('d', path);
  el.classList.add('polygon');
  svg.appendChild(el);

  el.addEventListener('click', () => {
    svg.querySelectorAll('path').forEach(p => p.classList.remove('selected'));
    el.classList.add('selected');
    document.querySelector('#info-panel h3').innerText = name;
    document.getElementById('pib').innerText = f.properties.pib_2021?.toLocaleString('pt-BR', {{ style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }}) || '-';
    document.getElementById('part').innerText = f.properties.participacao_rmc ? (f.properties.participacao_rmc * 100).toFixed(2) + '%' : '-';
    document.getElementById('percapita').innerText = f.properties.pib_per_capita?.toLocaleString('pt-BR', {{ style: 'currency', currency: 'BRL' }}) || '-';
    document.getElementById('pop').innerText = f.properties.populacao?.toLocaleString('pt-BR') || '-';
    document.getElementById('area').innerText = f.properties.area ? f.properties.area.toFixed(1).replace('.', ',') + ' km²' : '-';
    document.getElementById('dens').innerText = f.properties.densidade_demografica?.toFixed(1).replace('.', ',') + ' hab/km²' || '-';
    info.style.display = 'block';
  });

  const item = document.createElement('div');
  item.innerText = name;
  item.style.cursor = 'pointer';
  item.style.marginBottom = '6px';
  item.style.fontSize = '14px';
  item.style.color = '#0b3d91';
  item.addEventListener('click', () => el.dispatchEvent(new Event('click')));
  legend.appendChild(item);
});
</script>
</body>
</html>
""" width="100%" height="700px"></iframe>
"""

# INSERE O HTML INTERATIVO
st.components.v1.html(html_code, height=700, scrolling=False)
