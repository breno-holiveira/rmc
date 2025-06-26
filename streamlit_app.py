import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide")

# === Estilo refinado e quente (harmonizado com HTML e abas) ===
st.markdown("""
<style>
/* Remove barra lateral, cabeçalho e rodapé */
[data-testid="stSidebar"], header, footer {
    display: none !important;
}
.block-container {
    padding-top: 1rem !important;
}

/* Remove linha laranja padrão das abas */
div[data-testid="stTabs"] > div > div > div > div[aria-selected="true"]::after {
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Fundo suave em tons quentes */
body, .main {
    background: linear-gradient(120deg, #fff8f9, #fceeee);
}

/* Cor das abas */
div[data-testid="stTabs"] button {
    background-color: transparent !important;
    color: #994455 !important;
    font-weight: 500;
    border-radius: 0 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    border-bottom: 3px solid #f63366 !important;
    color: #f63366 !important;
}

/* Títulos e textos */
h1, h2, h3, h4, h5, h6 {
    color: #994455 !important;
}
p, span, label, div, li {
    color: #2e2e2e;
    font-size: 15px;
}

/* DataFrame refinado */
[data-testid="stDataFrame"] {
    border: 1px solid #f2c5cb;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* Gráficos com borda leve */
.css-1y0tads .stPlotlyChart, .stAltairChart, .stBarChart {
    background: white !important;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Links e interações */
a {
    color: #f63366;
}
</style>
""", unsafe_allow_html=True)

# === Abas no topo ===
abas = st.tabs(["Início", "PIB por Município", "Demografia", "Comparativo"])

# === Funções de carregamento com cache ===
@st.cache_data
def carregar_df():
    df = pd.read_excel('dados_rmc.xlsx')
    df.set_index("nome", inplace=True)
    return df

@st.cache_data
def carregar_gdf():
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    return gdf.sort_values(by='NM_MUN')

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

@st.cache_resource
def carregar_html_base():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

# === Conteúdo de cada aba ===
with abas[0]:
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    geojson_js = construir_geojson()
    html_template = carregar_html_base()
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

with abas[1]:
    st.header("PIB por Município")
    st.dataframe(carregar_df()[["PIB (2021)"]])

with abas[2]:
    st.header("Demografia")
    st.dataframe(carregar_df()[["populacao", "área", "densidade"]])

with abas[3]:
    st.header("Comparativo")
    df = carregar_df()
    st.bar_chart(df["PIB (2021)"].sort_values(ascending=False))
