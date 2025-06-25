import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="collapsed")

# ====== MENU SUPERIOR HORIZONTAL ======
menu_items = {
    "Início": "",
    "Página 1": "pag1",
    "Página 2": "pag2",
    "Página 3": "pag3"
}

st.markdown("""
<style>
    .menu-container {
        background: #111827;
        padding: 12px 24px;
        display: flex;
        justify-content: left;
        gap: 30px;
        font-family: sans-serif;
        font-size: 16px;
    }
    .menu-container a {
        color: #fff;
        text-decoration: none;
        padding: 6px 12px;
        border-radius: 6px;
        transition: background 0.3s;
    }
    .menu-container a:hover {
        background: rgba(255,255,255,0.1);
    }
</style>
<div class="menu-container">
""" + "\n".join([
    f'<a href="/?page={menu_items[label]}" target="_self">{label}</a>'
    for label in menu_items
]) + "</div>", unsafe_allow_html=True)

# ====== ROTEAMENTO COM BASE NA URL ======
query_params = st.experimental_get_query_params()
page = query_params.get("page", [""])[0]

if page == "":
    # PÁGINA INICIAL COM O MAPA INTERATIVO
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    # Carregamento dos dados
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    gdf = gdf.sort_values(by='NM_MUN')

    df = pd.read_excel('dados_rmc.xlsx')
    df.set_index("nome", inplace=True)

    # GeoJSON
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})

    gj = {"type": "FeatureCollection", "features": features}
    geojson_js = json.dumps(gj)

    # Carregamento do HTML
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        html_template = f.read()
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

    st.components.v1.html(html_code, height=600, scrolling=False)

elif page == "pag1":
    st.switch_page("pages/pag1.py")

elif page == "pag2":
    st.switch_page("pages/pag2.py")

elif page == "pag3":
    st.switch_page("pages/pag3.py")

else:
    st.error("Página não encontrada.")
