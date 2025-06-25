import streamlit as st
import pandas as pd
import geopandas as gpd
import json

import pages.pag1 as pag1
import pages.pag2 as pag2
import pages.pag3 as pag3

st.set_page_config(
    page_title="RMC Data",
    layout="wide"
)

# Remove a barra lateral de verdade e expande o conteúdo
hide_sidebar_style = """
<style>
    div[data-testid="stSidebar"] {display: none;}
    div[data-testid="stAppViewContainer"] > .main > div:first-child {
        max-width: 100% !important;
        padding-left: 1rem !important;
    }
</style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Obtem página via query_params
params = st.query_params
page = params.get("page", [""])[0]

menu_items = {
    "Início": "",
    "Página 1": "pag1",
    "Página 2": "pag2",
    "Página 3": "pag3"
}

# Menu fixo, estilizado e funcional
st.markdown(f"""
<style>
    .menu-container {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        background: #22272e;
        padding: 14px 30px;
        display: flex;
        gap: 24px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 16px;
        border-bottom: 1px solid #444c56;
        box-shadow: 0 2px 8px rgb(0 0 0 / 0.2);
    }}
    .menu-container a {{
        color: #cdd9e5;
        text-decoration: none;
        padding: 8px 16px;
        border-radius: 8px;
        transition: background-color 0.3s ease, color 0.3s ease;
        user-select: none;
        cursor: pointer;
    }}
    .menu-container a:hover {{
        background-color: #58a6ff;
        color: white;
    }}
    .menu-container a.active {{
        background-color: #0f62fe;
        color: white;
        font-weight: 600;
    }}
    /* espaço para conteúdo abaixo do menu fixo */
    .app-content {{
        padding-top: 64px;
        max-width: 1200px;
        margin: auto;
    }}
</style>

<div class="menu-container">
""" + "\n".join([
    f'<a href="/?page={v}" class="{"active" if page == v else ""}">{k}</a>'
    for k, v in menu_items.items()
]) + "</div>" + """
<div class='app-content'>
""", unsafe_allow_html=True)

# Funções cacheadas para desempenho (igual antes)

@st.cache_data(show_spinner=False)
def carregar_df():
    df = pd.read_excel("dados_rmc.xlsx")
    df.set_index("nome", inplace=True)
    return df

@st.cache_data(show_spinner=False)
def carregar_gdf():
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    return gdf.sort_values(by='NM_MUN')

@st.cache_resource(show_spinner=False)
def carregar_html_base():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

@st.cache_data(show_spinner=False)
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

# Roteamento de páginas

if page == "":
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

st.markdown("</div>", unsafe_allow_html=True)
