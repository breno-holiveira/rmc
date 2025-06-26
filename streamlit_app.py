import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Esconder barra lateral e topo padrão Streamlit
hide_streamlit_style = """
    <style>
        /* Remove sidebar */
        [data-testid="stSidebar"] {display: none !important;}
        /* Remove menu superior (header do Streamlit com Fork/Github) */
        header {display: none !important;}
        /* Remove rodapé */
        footer {display: none !important;}
        /* Ajusta container principal sem padding esquerdo e superior */
        .css-1d391kg {
            padding-left: 0 !important;
            padding-top: 0 !important;
        }
        /* Remove margem padrão da main block container */
        .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        /* Remove barra laranja padrão das tabs Streamlit */
        div[role="tablist"] > button[aria-selected="true"] {
            border-bottom: 3.5px solid transparent !important;
            box-shadow: none !important;
        }
        /* Container das abas - deixa grudado no topo e sem margem */
        div[role="tablist"] {
            display: flex !important;
            gap: 16px !important;
            padding: 14px 28px !important;
            background: rgba(20, 35, 55, 0.9) !important;
            border-radius: 14px 14px 0 0 !important;
            margin: 0 !important;
            position: sticky !important;
            top: 0 !important;
            z-index: 9999 !important;
            box-shadow: 0 2px 8px rgb(0 0 0 / 0.12) !important;
            user-select: none !important;
        }
        /* Abas individuais */
        div[role="tablist"] > button {
            background: transparent !important;
            color: #a0b8d9 !important;
            border: none !important;
            border-bottom: 3.5px solid transparent !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            padding: 12px 28px !important;
            border-radius: 10px 10px 0 0 !important;
            transition: color 0.3s ease, border-bottom-color 0.3s ease, background-color 0.25s ease;
            cursor: pointer !important;
        }
        /* Aba ativa */
        div[role="tablist"] > button[aria-selected="true"] {
            color: #3f5c85 !important;
            border-bottom: 3.5px solid #3f5c85 !important;
            background-color: rgba(63, 92, 133, 0.14) !important;
            font-weight: 700 !important;
            box-shadow: 0 3px 8px rgb(63 92 133 / 0.22) !important;
        }
        /* Hover abas não ativas */
        div[role="tablist"] > button:not([aria-selected="true"]):hover {
            color: #5a7ca6 !important;
            background-color: rgba(90, 124, 166, 0.1) !important;
            border-bottom-color: #5a7ca6 !important;
        }
        /* Conteúdo das abas */
        .css-1d391kg > div[role="tabpanel"] {
            background-color: #f2f6fb !important;
            border-radius: 0 14px 14px 14px !important;
            padding: 30px 36px !important;
            box-shadow: 0 6px 20px rgb(63 92 133 / 0.12) !important;
            border: 1.5px solid rgba(63, 92, 133, 0.12) !important;
            margin-bottom: 48px !important;
        }
        /* Fonte geral */
        html, body, .block-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            color: #223344 !important;
            background-color: #e8edf4 !important;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title="RMC Data", layout="wide")

@st.cache_data(show_spinner=False)
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

@st.cache_resource(show_spinner=False)
def carregar_html_template():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

html_template = carregar_html_template()

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
