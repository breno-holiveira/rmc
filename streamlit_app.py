import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide", page_icon='📊', initial_sidebar_state="expanded")

from streamlit_navigation_bar import st_navbar

page = st_navbar(["Home", "Documentation", "Examples", "Community", "About"])
st.write(page)

st.title("RMC Data 📊")
st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

st.markdown('A Região Metropolitana de Campinas foi criada em 2000, através da Lei Complementar nº 870, do estado de São Paulo e é constituida por 20 municípios. Em 2021, a RMC apresentou um PIB de 266,8 bilhões de reais, o equivalente a 3,07% do Produto Interno Bruto brasileiro no mesmo ano.')

st.markdown('Em 2020, o Instituo Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de Campinas como uma das 15 metrópoles brasileiras.')

# Carregamento de dados
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != 'EPSG:4326':
    gdf = gdf.to_crs('EPSG:4326')
gdf = gdf.sort_values(by='NM_MUN')

df = pd.read_excel('dados_rmc.xlsx')
df.set_index("nome", inplace=True)

# Construir GeoJSON (chaves normais aqui)
features = []
for _, row in gdf.iterrows():
    nome = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    props = df.loc[nome].to_dict() if nome in df.index else {}
    props["name"] = nome
    features.append({"type": "Feature", "geometry": geom, "properties": props})

gj = {"type": "FeatureCollection", "features": features}
geojson_js = json.dumps(gj)

# Carregamento de HTML externo refinado
with open("grafico_rmc.html", "r", encoding="utf-8") as f:
    html_template = f.read()

# Inserção do GeoJSON no HTML
html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

# Exibir no Streamlit
st.components.v1.html(html_code, height=600, scrolling=False)
