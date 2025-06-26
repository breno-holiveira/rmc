import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

st.markdown("""
<style>
/* Remover sidebar, header e footer */
[data-testid="stSidebar"], header, footer {
    display: none !important;
}
.block-container {
    padding-top: 0rem !important;
}

/* Container das abas */
div[data-testid="stTabs"] > div > div {
    padding: 8px 20px;
    display: flex;
    gap: 16px;
    border-bottom: 1.5px solid #ddd;  /* linha clara e única */
    background-color: white;
}

/* Cada aba */
div[data-testid="stTabs"] > div > div > div {
    color: #444; /* texto cinza escuro */
    font-weight: 600;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 16px;
    padding: 10px 24px;
    border-radius: 8px 8px 0 0;
    user-select: none;
    transition: color 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    cursor: pointer;
    border: 1.5px solid transparent; /* contorno suave invisível */
    border-bottom: none; /* tirar borda inferior da aba */
}

/* Aba ativa */
div[data-testid="stTabs"] > div > div > div[aria-selected="true"] {
    background-color: #f5f7fa;  /* fundo muito leve */
    color: #0d47a1; /* azul escuro profissional */
    border-color: #0d47a1; /* contorno azul */
    border-bottom: none !important; /* sem linha debaixo */
    box-shadow: 0 4px 12px rgb(13 71 161 / 0.15);
}

/* Hover nas abas não ativas - só texto azul, sem background */
div[data-testid="stTabs"] > div > div > div:not([aria-selected="true"]):hover {
    color: #0d47a1;
    background-color: transparent !important;
    border-color: #0d47a1; /* contorno azul leve no hover */
}

/* Remover underline laranja padrão */
div[data-testid="stTabs"] > div > div > div[aria-selected="true"]::after {
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Remover linhas extras */
div[data-testid="stTabs"] > div > div > div:not([aria-selected="true"]) {
    border-bottom: none !important;
}
</style>
""", unsafe_allow_html=True)

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
