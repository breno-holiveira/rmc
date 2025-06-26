import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

# === CSS refinado ===
st.markdown("""
<style>
/* Remove borda laranja residual com !important universal */
button[kind="tab"] {
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Estilo da barra de navegação por abas */
div[role="tablist"] {
    background-color: #1f2f45 !important;
    padding: 12px 24px !important;
    border-radius: 12px 12px 0 0 !important;
    display: flex !important;
    justify-content: flex-start;
    gap: 18px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    position: sticky !important;
    top: 0;
    z-index: 9999;
    margin-bottom: 0 !important;
}

/* Abas inativas */
div[role="tablist"] > button {
    background-color: transparent !important;
    color: #b0c7dd !important;
    font-size: 15px !important;
    padding: 10px 20px !important;
    border: none !important;
    border-radius: 8px 8px 0 0 !important;
    transition: all 0.3s ease;
}

/* Aba ativa */
div[role="tablist"] > button[aria-selected="true"] {
    background-color: #2a3e5c !important;
    color: #ffffff !important;
    border-bottom: 3px solid #2a3e5c !important;
    font-weight: 700;
}

/* Hover */
div[role="tablist"] > button:hover {
    background-color: rgba(255, 255, 255, 0.06) !important;
}

/* Conteúdo das abas */
.css-1d391kg > div[role="tabpanel"] {
    background-color: #f2f6fb !important;
    padding: 30px 36px;
    border-radius: 0 0 14px 14px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 6px 20px rgba(0,0,0,0.07);
}

/* Tipografia e layout */
html, body, .block-container {
    font-family: 'Segoe UI', sans-serif;
    background-color: #e8edf4;
    color: #223344;
}

/* Remove barra lateral e topo */
[data-testid="stSidebar"] { display: none !important; }
header { display: none !important; }
footer { display: none !important; }
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# === Dados ===
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
def carregar_html_template():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

def construir_geojson(gdf, df):
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    return {"type": "FeatureCollection", "features": features}

gdf, df = carregar_dados()
geojson_js = json.dumps(construir_geojson(gdf, df))
html_template = carregar_html_template()

# === Abas ===
tab1, tab2, tab3 = st.tabs(["Mapa RMC", "Página 1", "Página 2"])

with tab1:
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

with tab2:
    st.title("Página 1")
    st.write("Conteúdo e análises da Página 1 aqui.")

with tab3:
    st.title("Página 2")
    st.write("Conteúdo e análises da Página 2 aqui.")
