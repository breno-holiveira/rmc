import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Importação das páginas
import pages.pag1 as pag1
import pages.pag2 as pag2
import pages.pag3 as pag3

# Configuração inicial
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== PARÂMETROS DE ROTEAMENTO ======
params = st.query_params
page = params.get("page", "")

# ====== MENU HORIZONTAL GLASS ======
menu_items = {
    "Início": "",
    "Página 1": "pag1",
    "Página 2": "pag2",
    "Página 3": "pag3"
}

st.markdown(f"""
<style>
.menu-container {{
    position: sticky;
    top: 0;
    z-index: 999;
    backdrop-filter: blur(12px);
    background: rgba(255, 255, 255, 0.1);
    padding: 12px 24px;
    margin-bottom: 12px;
    display: flex;
    gap: 24px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}}

.menu-container a {{
    color: #e5e7eb;
    text-decoration: none;
    padding: 6px 16px;
    border-radius: 8px;
    transition: background 0.3s, color 0.3s;
}}

.menu-container a:hover {{
    background: rgba(255, 255, 255, 0.07);
}}

.menu-container .active {{
    background: rgba(255, 255, 255, 0.14);
    color: #ffffff;
}}
</style>

<div class="menu-container">
""" + "\n".join([
    f'<a href="/?page={v}" target="_self" class="{"active" if page == v else ""}">{k}</a>'
    for k, v in menu_items.items()
]) + "</div>", unsafe_allow_html=True)

# ====== FUNÇÕES CACHEADAS ======

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
def construir_geojson():
    gdf = carregar_gdf()
    df = carregar_df()
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": props
        })
    return json.dumps({"type": "FeatureCollection", "features": features})

# ====== ROTEAMENTO DAS PÁGINAS ======

if page == "":
    # Página inicial com mapa
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    geojson_js = construir_geojson()
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
