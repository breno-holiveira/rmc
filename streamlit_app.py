import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

# === Carregar dados com cache para acelerar ===
@st.cache_data(show_spinner=False)
def carregar_dados():
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    gdf = gdf.sort_values(by='NM_MUN')

    df = pd.read_excel('dados_rmc.xlsx')
    df.set_index("nome", inplace=True)
    return gdf, df

@st.cache_resource(show_spinner=False)
def carregar_html():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

gdf, df = carregar_dados()
html_template = carregar_html()

# === Construção do GeoJSON para o gráfico ===
def construir_geojson(gdf, df):
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    return json.dumps({"type": "FeatureCollection", "features": features})

geojson_js = construir_geojson(gdf, df)
html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

# === Menu simples para navegar ===
st.title("RMC Data")
st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

menu = st.radio("Selecione a página:", ["Mapa Interativo", "Página 1", "Página 2", "Página 3"], horizontal=True)

if menu == "Mapa Interativo":
    st.components.v1.html(html_code, height=600, scrolling=False)

elif menu == "Página 1":
    st.write("Aqui vai o conteúdo da Página 1")
    # Ou importe e chame sua função pag1.main() se quiser

elif menu == "Página 2":
    st.write("Aqui vai o conteúdo da Página 2")
    # pag2.main()

elif menu == "Página 3":
    st.write("Aqui vai o conteúdo da Página 3")
    # pag3.main()
