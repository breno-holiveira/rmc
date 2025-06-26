import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

# CSS para remover sidebar, header e footer e ajustar padding
st.markdown("""
<style>
/* Esconder barra lateral completamente */
[data-testid="stSidebar"] {
    display: none !important;
}

/* Esconder header (inclui GitHub fork e demais) */
header {
    display: none !important;
}

/* Esconder rodapé */
footer {
    display: none !important;
}

/* Ajustar padding do container principal para cima */
.block-container {
    padding-top: 0rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

# Exemplo de navegação com abas logo no topo
abas = st.tabs(["Início", "Página 1", "Página 2", "Página 3"])

with abas[0]:
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    # Exemplo de carregamento de dados e gráfico simplificado
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    gdf = gdf.sort_values(by='NM_MUN')

    df = pd.read_excel('dados_rmc.xlsx')
    df.set_index("nome", inplace=True)

    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})

    gj = {"type": "FeatureCollection", "features": features}
    geojson_js = json.dumps(gj)

    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

with abas[1]:
    st.header("Página 1")
    st.write("Conteúdo da Página 1")

with abas[2]:
    st.header("Página 2")
    st.write("Conteúdo da Página 2")

with abas[3]:
    st.header("Página 3")
    st.write("Conteúdo da Página 3")
