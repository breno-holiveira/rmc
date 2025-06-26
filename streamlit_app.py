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

st.markdown(
    """
    <style>
    /* --- Estilo customizado das abas --- */
    /* Remove borda padrão das tabs */
    .css-1d391kg .st-cXcYtU { 
        border-bottom: none !important;
    }

    /* Container das abas */
    div[role="tablist"] {
        display: flex;
        gap: 16px;
        padding: 12px 24px;
        background: rgba(30, 60, 90, 0.25); /* vidro fosco azul claro */
        backdrop-filter: saturate(180%) blur(10px);
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgb(20 40 80 / 0.1);
    }

    /* Abas individuais */
    div[role="tablist"] > button {
        background: transparent !important;
        color: #a9c0ff !important;  /* azul claro */
        border: none !important;
        border-bottom: 3px solid transparent !important;
        font-weight: 600 !important;
        font-size: 17px !important;
        padding: 10px 26px !important;
        border-radius: 8px 8px 0 0 !important;
        transition:
            color 0.35s ease,
            border-bottom-color 0.35s ease,
            background-color 0.3s ease;
        cursor: pointer;
    }

    /* Aba ativa */
    div[role="tablist"] > button[aria-selected="true"] {
        color: #1e40af !important; /* azul forte */
        border-bottom-color: #1e40af !important;
        background-color: rgba(30, 64, 175, 0.1) !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 12px rgb(30 64 175 / 0.25);
    }

    /* Hover abas não ativas */
    div[role="tablist"] > button:not([aria-selected="true"]):hover {
        color: #3b82f6 !important; /* azul médio */
        background-color: rgba(59, 130, 246, 0.1) !important;
        border-bottom-color: #3b82f6 !important;
    }

    /* Conteúdo da aba */
    .css-1d391kg > div[role="tabpanel"] {
        background-color: #f9fbff !important;
        border-radius: 0 12px 12px 12px !important;
        padding: 28px 32px !important;
        box-shadow: 0 8px 30px rgb(30 64 175 / 0.1);
        border: 1.5px solid rgba(30, 64, 175, 0.15) !important;
        margin-bottom: 40px;
    }

    /* Scrollbar para conteúdo da aba (se necessário) */
    .css-1d391kg > div[role="tabpanel"]::-webkit-scrollbar {
        width: 10px;
    }
    .css-1d391kg > div[role="tabpanel"]::-webkit-scrollbar-thumb {
        background-color: rgba(30, 64, 175, 0.3);
        border-radius: 6px;
    }
    .css-1d391kg > div[role="tabpanel"]::-webkit-scrollbar-track {
        background-color: transparent;
    }

    /* Fonte geral */
    html, body, .block-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1e293b;
        background-color: #f0f4ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
