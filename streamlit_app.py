import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Importa páginas
import pages.pag1 as pag1
import pages.pag2 as pag2
import pages.pag3 as pag3

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="collapsed")

# ===== MENU NAVBAR =====
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

# ====== ROTEAMENTO ======
params = st.query_params
page = params.get("page", "")

# === Funções com cache para desempenho ===
@st.cache_data
def carregar_df():
    df = pd.read_excel("dados_rmc.xlsx")
    df.set_index("nome", inplace=True)
    return df

@st.cache_data
def carregar_gdf():
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    return gdf.sort_values(by='NM_MUN')

@st.cache_resource
def carregar_html_base():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

@st.cache_data
def construir_geojson(gdf, df):
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    return json.dumps({"type": "FeatureCollection", "features": features})


# ==== Página Inicial ====
if page == "":
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    gdf = carregar_gdf()
    df = carregar_df()
    geojson_js = construir_geojson(gdf, df)
    html_template = carregar_html_base()

    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

elif page == "pag1":
    pag1.main()
elif page == "pag2":
    pag2.main()
elif page == "pag3":
    pag3.main()
else:
    st.error("Página não encontrada.")
