import streamlit as st
import pandas as pd
import geopandas as gpd
import json

import pages.pag1 as pag1
import pages.pag2 as pag2
import pages.pag3 as pag3

st.set_page_config(page_title="RMC Data", layout="wide")

# Remove barra lateral padrão do Streamlit
st.markdown("""
<style>
div[data-testid="stSidebar"] {display:none !important;}
div[data-testid="stAppViewContainer"] > .main > div:first-child {
    max-width: 100% !important;
    padding-left: 1rem !important;
}
/* Barra de navegação fixa horizontal */
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 50px;
    background-color: #ff6600;  /* laranja */
    display: flex;
    align-items: center;
    padding: 0 2rem;
    gap: 1.5rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    z-index: 9999;
    box-shadow: 0 4px 8px rgba(255,102,0,0.3);
    user-select: none;
}
.navbar a {
    color: white;
    text-decoration: none;
    padding: 0.4rem 1rem;
    border-radius: 8px;
    transition: background-color 0.3s ease;
}
.navbar a:hover {
    background-color: rgba(255,255,255,0.3);
}
.navbar a.active {
    background-color: #cc5200;
    box-shadow: 0 0 8px #cc5200;
}
/* Espaço para conteúdo abaixo da navbar */
.content {
    padding-top: 60px;
    max-width: 1200px;
    margin: 0 auto 2rem auto;
}
</style>
""", unsafe_allow_html=True)

# Lê o parâmetro "page" da URL usando API estável
params = st.query_params
page = params.get("page", ["home"])[0]

# Constroi HTML da navbar com o item ativo destacado dinamicamente
menu_html = f"""
<div class="navbar">
    <a href="/?page=home" class="{'active' if page == 'home' else ''}">Início</a>
    <a href="/?page=pag1" class="{'active' if page == 'pag1' else ''}">Página 1</a>
    <a href="/?page=pag2" class="{'active' if page == 'pag2' else ''}">Página 2</a>
    <a href="/?page=pag3" class="{'active' if page == 'pag3' else ''}">Página 3</a>
</div>
"""

st.components.v1.html(menu_html, height=50)

# Espaço para conteúdo
st.markdown('<div class="content">', unsafe_allow_html=True)

if page == "home":
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    @st.cache_data
    def carregar_dados():
        gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
        if gdf.crs != 'EPSG:4326':
            gdf = gdf.to_crs('EPSG:4326')
        gdf = gdf.sort_values(by='NM_MUN')

        df = pd.read_excel('dados_rmc.xlsx')
        df.set_index("nome", inplace=True)
        return gdf, df

    @st.cache_resource
    def carregar_html():
        with open("grafico_rmc.html", "r", encoding="utf-8") as f:
            return f.read()

    gdf, df = carregar_dados()
    html_template = carregar_html()

    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})

    geojson_js = json.dumps({"type": "FeatureCollection", "features": features})
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

    st.components.v1.html(html_code, height=600, scrolling=False)

elif page == "pag1":
    pag1.main()
elif page == "pag2":
    pag2.main()
elif page == "pag3":
    pag3.main()
else:
    st.error("Página não encontrada.")

st.markdown("</div>", unsafe_allow_html=True)
