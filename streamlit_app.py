import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from pathlib import Path

# CONFIGURAÇÕES DA PÁGINA INICIAL
st.set_page_config(
    page_title='RMC Data',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# TÍTULO
st.markdown('# RMC Data')
st.markdown('## Dados e indicadores da Região Metropolitana de Campinas')

# SHAPEFILE
gdf = gpd.read_file('./shapefile_rmc/RMC_municipios.shp')
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

# DADOS DO SHAPEFILE
df_dados = pd.read_excel('dados_rmc.xlsx')
df_dados.set_index("nome", inplace=True)

features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__

    if nome in df_dados.index:
        dados = df_dados.loc[nome]
        feature_props = {
            "name": nome,
            "pib_2021": dados["pib_2021"],
            "participacao_rmc": dados["participacao_rmc"],
            "pib_per_capita": dados["per_capita_2021"],
            "populacao": dados["populacao_2022"],
            "area": dados["area"],
            "densidade_demografica": dados["densidade_demografica_2022"]
        }
    else:
        feature_props = {
            "name": nome,
            "pib_2021": None,
            "participacao_rmc": None,
            "pib_per_capita": None,
            "populacao": None,
            "area": None,
            "densidade_demografica": None
        }

    features.append({
        "type": "Feature",
        "properties": feature_props,
        "geometry": geom
    })

geojson = {"type": "FeatureCollection", "features": features}
geojson_str = json.dumps(geojson)

# HTML/JS para o mapa interativo embutido no Streamlit

html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<title>Mapa Interativo RMC - Transparência</title>
<style>
  *, *::before, *::after {
    box-sizing: border-box;
  }
  html, body {
    margin: 0; padding: 0;
    height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    background-color: transparent;
    color: #222;
    display: grid;
    grid-template-columns: 230px 1fr 350px;
    grid-template-rows: 1fr;
    gap: 12px;
    padding: 12px;
    width: 100vw;
    height: 100vh;
    background: #f9f9f9;
  }

  #legend {
    background: #fff;
    padding: 16px 20px;
    box-shadow: 2px 0 8px rgba(0,0,0,0.08);
    border-radius: 10px;
    border: 1px solid #e3e6ea;
    overflow-y: auto;
    font-size: 14px;
  }
  #legend strong {
    display: block;
    font-weight: 700;
    font-size: 18px;
    margin-bottom: 12px;
    color: #0b3d91;
    border-bottom: 2px solid #0b3d91;
    padding-bottom: 6px;
  }
  #legend div {
    margin-bottom: 8px;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
    color: #3a3a3a;
    white-space: nowrap;
  }
  #legend div:hover {
    background-color: #dbe7fd;
    color: #08318d;
  }
  #legend div.active {
    background-color: #0b3d91;
    color: #fff;
    font-weight: 700;
  }

  #map {
    position: relative;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    overflow: hidden;
  }
  svg {
    width: 100%;
    height: 100vh;
    display: block;
    user-select: none;
  }

  #info-panel {
    background: #fff;
    padding: 20px 24px 32px 24px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    color: #333;
    font-size: 15px;
    line-height: 1.5;
    overflow-y: auto;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  #info-panel.visible {
    display: flex;
  }
  #info-panel h3 {
    margin-top: 0;
    font-weight: 700;
    font-size: 18px;
    color: #0b3d91;
    border-bottom: 2px solid #0b3d91;
    padding-bottom: 8px;
    margin-bottom: 16px;
  }
  #info-panel div {
    margin-bottom: 14px;
    display: flex;
    flex-direction: column;
  }
  #info-panel div strong {
    display: block;
    color: #0b3d91;
    margin-bottom: 4px;
    white-space: normal;
  }
  #info-panel div span {
    color: #333;
    font-weight: 600;
    font-size: 1rem;
    white-space: normal;
  }
  #info-panel footer {
    margin-top: auto;
    font-size: 12px;
    color: #666;
    text-align: right;
    font-style: italic;
  }
  #info-panel button#close-info {
    align-self: flex-end;
    background: transparent;
    border: none;
    font-size: 22px;
    color: #0b3d91;
    cursor: pointer;
    font-weight: 700;
    margin-bottom: 12px;
    padding: 0;
    line-height: 1;
  }
  #info-panel button#close-info:hover {
    color: #08318d;
  }

  #tooltip {
    position: absolute;
    pointer-events: none;
    padding: 6px 12px;
    background: rgba(11, 61, 145, 0.9);
    color: #fefefe;
    font-weight: 600;
    font-size: 12px;
    border-radius: 5px;
    white-space: nowrap;
    box-shadow: 0 0 6px rgba(11, 61, 145, 0.5);
    display: none;
    user-select: none;
    z-index: 1000;
  }

  .polygon {
    fill: rgba(11, 61, 145, 0.15);
    stroke: rgba(11, 61, 145, 0.6);
    stroke-width: 1;
    cursor: pointer;
    transition: fill 0.25s ease, stroke 0.25s ease;
    opacity: 0.85;
  }
  .polygon:hover {
    fill: rgba(11, 61, 145, 0.35);
    stroke-width: 2;
    filter: drop-shadow(0 0 6px rgba(11, 61, 145, 0.3));
  }
  .polygon.selected {
    fill: rgba(11, 61, 145, 0.45);
    stroke: rgba(11, 61, 145, 0.8);
    stroke-width: 2.5;
    filter: drop-shadow(0 0 10px rgba(11, 61, 145, 0.5));
  }
</style>
</head>
<body>
  <nav id="legend">
    <strong>Municípios da RMC</strong>
    <div id="mun-list"></div>
  </nav>
  <main id="map">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg"></svg>
    <div id="tooltip"></div>
  </main>
  <aside id="info-panel">
    <button id="close-info">&times;</button>
    <h3>Selecione um município</h3>
    <div><strong>PIB (2021):</strong> <span>-</span></div>
    <div><strong>Participação na RMC:</strong> <span>-</span></div>
    <div><strong>PIB per capita (2021):</strong> <span>-</span></div>
    <div><strong>População:</strong> <span>-</span></div>
    <div><strong>Área:</strong> <span>-</span></div>
    <div><strong>Densidade demográfica (2022):</strong> <span>-</span></div>
    <footer>Fonte: IBGE Cidades</footer>
  </aside>
</body>
</html>
"""

# Renderiza o HTML no Streamlit
st.components.v1.html(html_code, height=650, scrolling=True)
