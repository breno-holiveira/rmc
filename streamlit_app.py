import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

# Oculta barra lateral mesmo (com CSS)
hide_sidebar_css = """
<style>
    div[data-testid="stSidebar"] {display: none;}
</style>
"""
st.markdown(hide_sidebar_css, unsafe_allow_html=True)

# Função para carregar dados com cache
@st.cache_data
def carregar_dados():
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    gdf = gdf.sort_values(by='NM_MUN')

    df = pd.read_excel('dados_rmc.xlsx')
    df.set_index("nome", inplace=True)
    return gdf, df

gdf, df = carregar_dados()

# Construir GeoJSON
def construir_geojson(gdf, df):
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    return {"type": "FeatureCollection", "features": features}

geojson_dict = construir_geojson(gdf, df)
geojson_js = json.dumps(geojson_dict)

# Carregar template HTML (com cache)
@st.cache_resource
def carregar_html_template():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

html_template = carregar_html_template()

# Menu - páginas e labels
pages = {
    "home": "Início",
    "pag1": "Página 1",
    "pag2": "Página 2"
}

# Pegar página da query params (st.query_params, não experimental)
query_params = st.query_params
current_page = query_params.get("page", ["home"])[0]

# Barra de navegação estilizada
nav_css = """
<style>
.navbar {
    display: flex;
    gap: 20px;
    background-color: #222;
    padding: 12px 30px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 600;
    font-size: 16px;
    user-select: none;
    position: sticky;
    top: 0;
    z-index: 9999;
}
.navbar a {
    color: #bbb;
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 5px;
    transition: background-color 0.25s ease, color 0.25s ease;
}
.navbar a:hover {
    background-color: #ff7f50;  /* coral laranja suave */
    color: white;
}
.navbar a.active {
    background-color: #ff4500;  /* laranja forte */
    color: white;
    font-weight: 700;
}
</style>
"""

# Construir html da navbar com links e active class
nav_html = '<div class="navbar">'
for key, label in pages.items():
    active_class = "active" if key == current_page else ""
    nav_html += f'<a href="/?page={key}" class="{active_class}">{label}</a>'
nav_html += "</div>"

# Exibir barra de navegação
st.markdown(nav_css + nav_html, unsafe_allow_html=True)

# Conteúdo conforme página selecionada
if current_page == "home":
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

elif current_page == "pag1":
    st.title("Página 1")
    st.write("Conteúdo e análises da Página 1 aqui.")

elif current_page == "pag2":
    st.title("Página 2")
    st.write("Conteúdo e análises da Página 2 aqui.")

else:
    st.error("Página não encontrada.")
