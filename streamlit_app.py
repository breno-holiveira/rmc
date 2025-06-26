import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Configurações da página
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# Remover menu, rodapé e GitHub
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
    }
    </style>
""", unsafe_allow_html=True)

# Estilo profissional da navbar
style = {
    "txColor": "#f0f0f0",
    "txColorHover": "#ff7200",
    "bgColor": "#0d1f3c",
    "bgColorHover": "#163466",
    "bgColorActive": "#ff7200",
    "txColorActive": "#ffffff",
    "height": 52,
    "font": "Roboto, sans-serif",
    "fontWeight": "600",
    "iconName": "📊",
    "iconSize": 22,
    "iconColor": "#ff7200",
    "iconColorActive": "#ffffff",
    "optionsSeparator": "|||",
}

# Criação da barra de navegação estilizada
selected = st_navbar(
    options=["Home", "Documentation", "Examples", "Community", "About"],
    style=style
)

# Exibição condicional das páginas
if selected == "Home":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

    st.markdown(
        "A Região Metropolitana de Campinas foi criada em 2000, através da Lei Complementar nº 870, do estado de São Paulo e é constituída por 20 municípios. "
        "Em 2021, a RMC apresentou um PIB de 266,8 bilhões de reais, o equivalente a 3,07% do Produto Interno Bruto brasileiro no mesmo ano."
    )
    st.markdown(
        "Em 2020, o Instituto Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de Campinas como uma das 15 metrópoles brasileiras."
    )

    # Dados
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values(by="NM_MUN")

    df = pd.read_excel("dados_rmc.xlsx")
    df.set_index("nome", inplace=True)

    # GeoJSON
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    gj = {"type": "FeatureCollection", "features": features}
    geojson_js = json.dumps(gj)

    # HTML com mapa
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        html_template = f.read()
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

elif selected == "Documentation":
    st.title("📄 Documentação")
    st.write("Aqui você pode colocar a documentação do seu app...")

elif selected == "Examples":
    st.title("💡 Exemplos")
    st.write("Exemplos do app...")

elif selected == "Community":
    st.title("🌐 Comunidade")
    st.write("Links para a comunidade...")

elif selected == "About":
    st.title("ℹ️ Sobre")
    st.write("Informações sobre o projeto...")
