import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

# === CSS personalizado ===
st.markdown("""
<style>
/* Remove cabeçalho, rodapé e barra lateral */
header, footer, [data-testid="stSidebar"] {
    display: none !important;
}
.block-container {
    padding-top: 0 !important;
}

/* Estilização das abas */
div[role="tablist"] {
    background-color: #1e2a38;
    padding: 12px 24px;
    gap: 16px;
    border-radius: 12px 12px 0 0;
    box-shadow: 0 1px 6px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 999;
}

/* Todas as abas */
div[role="tablist"] > button {
    all: unset !important;
    padding: 10px 20px;
    font-size: 15px;
    color: #b5c7db;
    font-weight: 500;
    border-radius: 8px 8px 0 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

/* Hover */
div[role="tablist"] > button:hover {
    background-color: rgba(255, 255, 255, 0.08);
    color: #fff;
}

/* Aba ativa */
div[role="tablist"] > button[aria-selected="true"] {
    background-color: #27384c;
    color: #fff;
    font-weight: 700;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Remove borda inferior automática */
div[role="tablist"] > button[aria-selected="true"]::after {
    display: none !important;
}

/* Conteúdo da aba */
.css-1d391kg > div[role="tabpanel"] {
    background-color: #f3f6fa;
    padding: 36px 40px;
    border-radius: 0 0 12px 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    border: 1px solid #dde5ef;
}

/* Estilo base do site */
html, body {
    background-color: #e6ecf2;
    font-family: 'Segoe UI', sans-serif;
    color: #1c2b3a;
}
</style>
""", unsafe_allow_html=True)

# === Carregamento de dados
@st.cache_data(show_spinner=False)
def carregar_dados():
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values(by="NM_MUN")
    df = pd.read_excel("dados_rmc.xlsx")
    df.set_index("nome", inplace=True)
    return gdf, df

@st.cache_resource(show_spinner=False)
def carregar_html():
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
html_template = carregar_html()

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
