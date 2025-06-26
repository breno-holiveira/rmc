import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Configurações da página
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# Página ativa atual (armazenada em estado)
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

# Estilo profissionalizado da barra de navegação com "logo" texto
styles = {
    "nav": {
        "background-color": "#0d1f3c",
        "padding": "0.6rem 2rem",
        "justify-content": "center",
        "font-family": "'Segoe UI', 'Roboto', sans-serif",
        "font-size": "16px",
        "border-radius": "0 0 16px 16px",
        "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.25)",
        "position": "relative",
    },
    "span": {
        "color": "#ffffff",
        "padding": "10px 18px",
        "transition": "background-color 0.25s, color 0.25s",
        "border-radius": "10px",
    },
    "active": {
        "background-color": "#ff7200",
        "color": "white",
        "font-weight": "600",
        "padding": "10px 18px",
        "border-radius": "10px",
        "box-shadow": "0 0 6px rgba(255,114,0,0.5)",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Logo textual clicável no topo esquerdo
st.markdown("""
<style>
.logo-text {
    position: absolute;
    top: 0.65rem;
    left: 2rem;
    font-size: 1.4rem;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    color: white;
    font-weight: 600;
    z-index: 10000;
    cursor: pointer;
    transition: color 0.2s ease;
}
.logo-text:hover {
    color: #ff7200;
}
</style>
<a href="?nav=Home"><div class="logo-text">RMC DATA</div></a>
""", unsafe_allow_html=True)

# Barra de navegação
pages = ["Home", "Documentation", "Examples", "Community", "About"]
page = st_navbar(pages, styles=styles, options=options)

# Atualiza estado ao mudar aba
st.session_state.current_page = page

# Lógica de exibição das páginas
if page == "Home":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

    st.markdown(
        "A Região Metropolitana de Campinas foi criada em 2000, através da Lei Complementar nº 870, do estado de São Paulo e é constituída por 20 municípios. "
        "Em 2021, a RMC apresentou um PIB de 266,8 bilhões de reais, o equivalente a 3,07% do Produto Interno Bruto brasileiro no mesmo ano."
    )
    st.markdown(
        "Em 2020, o Instituto Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de Campinas como uma das 15 metrópoles brasileiras."
    )

    # Carregamento de dados
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values(by="NM_MUN")

    df = pd.read_excel("dados_rmc.xlsx")
    df.set_index("nome", inplace=True)

    # Construção do GeoJSON
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})

    gj = {"type": "FeatureCollection", "features": features}
    geojson_js = json.dumps(gj)

    # Carregar HTML refinado do mapa
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

elif page == "Documentation":
    st.title("Documentation")
    st.write("Aqui você pode colocar a documentação do seu app...")

elif page == "Examples":
    st.title("Examples")
    st.write("Exemplos do app...")

elif page == "Community":
    st.title("Community")
    st.write("Links para a comunidade...")

elif page == "About":
    st.title("About")
    st.write("Sobre o projeto...")
