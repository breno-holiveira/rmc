import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title='RMC Data',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('RMC Data')
st.markdown('## Dados e indicadores da Região Metropolitana de Campinas')

# SHAPEFILE
gdf = gpd.read_file('./shapefile_rmc/RMC_municipios.shp')
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

# DADOS DO EXCEL
df_dados = pd.read_excel('dados_rmc.xlsx')
df_dados.set_index("nome", inplace=True)

# GERAÇÃO DO GEOJSON
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__

    if nome in df_dados.index:
        dados = df_dados.loc[nome]
        props = {
            "name": nome,
            "pib_2021": dados["pib_2021"],
            "participacao_rmc": dados["participacao_rmc"],
            "pib_per_capita": dados["per_capita_2021"],
            "populacao": dados["populacao_2022"],
            "area": dados["area"],
            "densidade_demografica": dados["densidade_demografica_2022"]
        }
    else:
        props = {k: None for k in [
            "name", "pib_2021", "participacao_rmc", "pib_per_capita",
            "populacao", "area", "densidade_demografica"
        ]}
        props["name"] = nome

    features.append({
        "type": "Feature",
        "properties": props,
        "geometry": geom
    })

geojson_str = json.dumps({"type": "FeatureCollection", "features": features})

# HTML embutido
html_code = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Mapa Interativo RMC</title>
  <style>
    *, *::before, *::after {{
      box-sizing: border-box;
    }}
    html, body {{
      margin: 0;
      padding: 0;
      height: 100vh;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #f9f9f9;
      color: #222;
      overflow: hidden;
      display: grid;
      grid-template-columns: 220px 1fr auto;
      grid-template-rows: 100vh;
    }}
    #legend {{
      background: #fff;
      padding: 16px 20px;
      border-right: 1px solid #e0e0e0;
      overflow-y: auto;
      box-shadow: 2px 0 8px rgba(0,0,0,0.05);
    }}
    #legend strong {{
      display: block;
      font-weight: bold;
      font-size: 16px;
      color: #0b3d91;
      border-bottom: 1px solid #0b3d91;
      padding-bottom: 6px;
      margin-bottom: 12px;
    }}
    #legend div {{
      margin-bottom: 8px;
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 14px;
      color: #333;
      transition: background 0.3s;
    }}
    #legend div:hover {{
      background: #eef3fc;
    }}
    #legend div.active {{
      background-color: #0b3d91;
      color: #fff;
      font-weight: 700;
    }}
    #map {{
      position: relative;
      background: #fff;
    }}
    svg {{
      width: 100%;
      height: 100vh;
      display: block;
    }}
    #tooltip {{
      position: absolute;
      pointer-events: none;
      padding: 6px 12px;
      background: rgba(11, 61, 145, 0.9);
      color: #fff;
      font-weight: 600;
      font-size: 12px;
      border-radius: 5px;
      box-shadow: 0 0 6px rgba(11, 61, 145, 0.4);
      display: none;
      z-index: 1000;
    }}
    #info-panel {{
      background: #fff;
      padding: 20px 24px;
      width: 330px;
      box-shadow: 0 0 12px rgba(0,0,0,0.08);
      border-left: 1px solid #e0e0e0;
      overflow-y: auto;
      font-size: 15px;
      display: none;
      position: relative;
    }}
    #info-panel.visible {{
      display: block;
    }}
    #info-panel h3 {{
      margin-top: 0;
      font-size: 17px;
      color: #0b3d91;
      border-bottom: 2px solid #0b3d91;
      padding-bottom: 6px;
      margin-bottom: 16px;
    }}
    #info-panel div {{
      margin-bottom: 14px;
      display: flex;
      flex-direction: column;
    }}
    #info-panel div strong {{
      color: #0b3d91;
      font-weight: 600;
      margin-bottom: 2px;
    }}
    #info-panel div span {{
      color: #333;
      font-weight: 500;
      white-space: normal;
    }}
    #info-panel button#close-info {{
      position: absolute;
      top: 8px;
      right: 12px;
      background: none;
      border: none;
      font-size: 20px;
      color: #0b3d91;
      cursor: pointer;
    }}
    #info-panel .fonte {{
      font-size: 11px;
      color: #666;
      margin-top: 20px;
      text-align: right;
      font-style: italic;
    }}
    .polygon {{
      fill: rgba(11, 61, 145, 0.15);
      stroke: rgba(11, 61, 145, 0.6);
      stroke-width: 1;
      cursor: pointer;
      transition: all 0.3s ease;
    }}
    .polygon:hover {{
      fill: rgba(11, 61, 145, 0.3);
      stroke-width: 2;
      filter: drop-shadow(0 0 6px rgba(11, 61, 145, 0.25));
    }}
    .polygon.selected {{
      fill: rgba(11, 61, 145, 0.4);
      stroke: rgba(11, 61, 145, 0.8);
      stroke-width: 2.5;
      filter: drop-shadow(0 0 10px rgba(11, 61, 145, 0.5));
    }}
  </style>
</head>
<body>

  <nav id="legend" aria-label="Lista de municípios">
    <strong>Municípios da RMC</strong>
    <div id="mun-list"></div>
  </nav>

  <main id="map" aria-label="Mapa dos municípios">
    <svg viewBox="0 0 1000 950" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg"></svg>
    <div id="tooltip"></div>
  </main>

  <aside id="info-panel" aria-label="Informações do município">
    <button id="close-info" aria-label="Fechar painel">&times;</button>
    <h3>Selecione um município</h3>
    <div><strong>PIB (2021):</strong><span>-</span></div>
    <div><strong>Participação na RMC:</strong><span>-</span></div>
    <div><strong>PIB per capita (2021):</strong><span>-</span></div>
    <div><strong>População:</strong><span>-</span></div>
    <div><strong>Área:</strong><span>-</span></div>
    <div><strong>Densidade demográfica (2022):</strong><span>-</span></div>
    <div class="fonte">Fonte: IBGE Cidades</div>
  </aside>

</body>
</html>
"""

# MOSTRA NO STREAMLIT
st.components.v1.html(html_code, height=650, scrolling=True)
