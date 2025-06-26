import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")

# === CSS ===
st.markdown("""
<style>
/* Remove barra lateral, header e footer */
header, footer, [data-testid="stSidebar"] {
    display: none !important;
}
.block-container {
    padding-top: 0rem !important;
}

/* Estiliza abas com aparência de barra de navegação */
div[role="tablist"] {
    background-color: #1e2a38;
    padding: 12px 24px;
    gap: 16px;
    border-radius: 12px 12px 0 0;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.05);
    position: sticky;
    top: 0;
    z-index: 1000;
}

/* Botões das abas */
div[role="tablist"] > button {
    all: unset !important;
    padding: 10px 20px;
    font-size: 15px;
    color: #c5d5e2;
    font-weight: 500;
    border-radius: 8px 8px 0 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

/* Hover das abas */
div[role="tablist"] > button:hover {
    background-color: rgba(255,255,255,0.05);
    color: #ffffff;
}

/* Aba ativa */
div[role="tablist"] > button[aria-selected="true"] {
    background-color: #2a3d52;
    color: #ffffff;
    font-weight: 700;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* REMOVE a LINHA LARANJA de forma definitiva */
div[role="tablist"] > button[aria-selected="true"]::after {
    display: none !important;
    content: none !important;
    border: none !important;
    box-shadow: none !important;
}

/* Remove sombra e borda inferior do container */
div[role="tablist"] {
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Estilo da aba ativa */
.css-1d391kg > div[role="tabpanel"] {
    background-color: #f4f7fa;
    padding: 36px 40px;
    border-radius: 0 0 12px 12px;
    border: 1px solid #dde5ef;
}

/* Ajustes gerais */
html, body {
    background-color: #e6ecf2;
    font-family: 'Segoe UI', sans-serif;
    color: #1c2b3a;
}
</style>
""", unsafe_allow_html=True)

# === Carregamento dos dados ===
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

# === Processamento
gdf, df = carregar_dados()
geojson_js = json.dumps(construir_geojson(gdf, df))
html_template = carregar_html()

# === Abas horizontais
tab1, tab2, tab3 = st.tabs(["Mapa RMC", "Página 1", "Página 2"])

with tab1:
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

with tab2:
    st.title("Página 1")
    st.write("Conteúdo da página 1 aqui.")

with tab3:
    st.title("Página 2")
    st.write("Conteúdo da página 2 aqui.")
