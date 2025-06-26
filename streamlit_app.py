import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

# CSS para estilizar a barra de abas e remover sidebar/header
st.markdown("""
<style>
/* Remove barra lateral, header e footer */
[data-testid="stSidebar"], header, footer {
    display: none !important;
}
.block-container {
    padding-top: 0rem !important;
}

/* Container das abas */
div[data-testid="stTabs"] > div > div {
    background-color: #f97316;  /* laranja vibrante */
    padding: 8px 16px;
    border-radius: 8px;
    display: flex;
    gap: 10px;
    box-shadow: 0 3px 10px rgb(249 115 22 / 0.5);
}

/* Cada botão da aba */
div[data-testid="stTabs"] > div > div > div {
    color: white;
    font-weight: 600;
    padding: 8px 20px;
    border-radius: 6px;
    user-select: none;
    transition: background-color 0.25s ease, color 0.25s ease;
    cursor: pointer;
}

/* Aba ativa */
div[data-testid="stTabs"] > div > div > div[aria-selected="true"] {
    background-color: #c2410c;  /* laranja escuro */
    box-shadow: 0 0 8px rgb(156 40 0 / 0.8);
    color: #fff;
}

/* Hover nas abas não ativas */
div[data-testid="stTabs"] > div > div > div:not([aria-selected="true"]):hover {
    background-color: #ea580c;  /* laranja médio */
    color: #fff;
}

/* Remove linha laranja default do tab ativo */
div[data-testid="stTabs"] > div > div > div[aria-selected="true"]::after {
    border-bottom: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# Definição das abas
abas = st.tabs(["Início", "PIB por Município", "Demografia", "Comparativo"])

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
