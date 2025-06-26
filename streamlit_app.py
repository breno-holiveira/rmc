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
    /* Remove borda padrão das tabs */
    .css-1d391kg .st-cXcYtU { 
        border-bottom: none !important;
    }

    /* Container das abas */
    div[role="tablist"] {
        display: flex;
        gap: 16px;
        padding: 14px 28px;
        background: rgba(15, 33, 64, 0.85); /* azul escuro translúcido */
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 2px 10px rgb(0 0 0 / 0.15);
        user-select: none;
    }

    /* Abas individuais */
    div[role="tablist"] > button {
        background: transparent !important;
        color: #a7c0e8 !important;  /* azul claro */
        border: none !important;
        border-bottom: 3.5px solid transparent !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 12px 28px !important;
        border-radius: 10px 10px 0 0 !important;
        transition:
            color 0.3s ease,
            border-bottom-color 0.3s ease,
            background-color 0.25s ease;
        cursor: pointer;
    }

    /* Aba ativa */
    div[role="tablist"] > button[aria-selected="true"] {
        color: #4a90e2 !important; /* azul médio */
        border-bottom-color: #4a90e2 !important;
        background-color: rgba(74, 144, 226, 0.12) !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 8px rgb(74 144 226 / 0.25);
    }

    /* Hover abas não ativas */
    div[role="tablist"] > button:not([aria-selected="true"]):hover {
        color: #7aaefc !important; /* azul um pouco mais claro */
        background-color: rgba(122, 174, 252, 0.1) !important;
        border-bottom-color: #7aaefc !important;
    }

    /* Conteúdo da aba */
    .css-1d391kg > div[role="tabpanel"] {
        background-color: #f7faff !important;  /* fundo azul bem claro */
        border-radius: 0 14px 14px 14px !important;
        padding: 30px 36px !important;
        box-shadow: 0 6px 24px rgb(74 144 226 / 0.15);
        border: 1.5px solid rgba(74, 144, 226, 0.15) !important;
        margin-bottom: 48px;
    }

    /* Fonte geral */
    html, body, .block-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1a2738;
        background-color: #e9f0fc;
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
