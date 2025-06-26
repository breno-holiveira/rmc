import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

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

def construir_geojson(gdf, df):
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    return {"type": "FeatureCollection", "features": features}

geojson_js = json.dumps(construir_geojson(gdf, df))

@st.cache_resource
def carregar_html_template():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

html_template = carregar_html_template()

# --- Estilo customizado para as tabs ---
st.markdown(
    """
    <style>
    /* Esconde a barra padrão das tabs */
    .css-1d391kg .st-cXcYtU { 
        border-bottom: none !important;
    }
    /* Estiliza os botões das abas */
    div[role="tablist"] > button {
        background-color: #fff4e6 !important;  /* bege clarinho */
        color: #d35400 !important;             /* laranja suave */
        border: 1.5px solid #d35400 !important;
        border-bottom: none !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 10px 24px !important;
        margin-right: 6px !important;
        border-radius: 10px 10px 0 0 !important;
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    /* Aba ativa */
    div[role="tablist"] > button[aria-selected="true"] {
        background-color: #d35400 !important;  /* laranja forte */
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 8px rgba(211, 84, 0, 0.4);
    }
    /* Hover das abas não ativas */
    div[role="tablist"] > button:not([aria-selected="true"]):hover {
        background-color: #f5b041 !important; /* laranja claro hover */
        color: white !important;
        border-color: #f5b041 !important;
        cursor: pointer;
    }
    /* Conteúdo da aba */
    .css-1d391kg > div[role="tabpanel"] {
        border: 1.5px solid #d35400 !important;
        border-top: none !important;
        border-radius: 0 10px 10px 10px !important;
        padding: 20px !important;
        background-color: #fff9f0 !important;
        box-shadow: 0 0 12px rgb(211 84 0 / 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Criando as abas ---
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
