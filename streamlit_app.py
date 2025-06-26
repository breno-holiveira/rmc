import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# Estilo visual refinado com fonte Inter
styles = {
    "nav": {
        "background-color": "royalblue",
        "justify-content": "left",
        "font-family": "'Inter', 'Helvetica Neue', sans-serif",
        "font-size": "16px",
    },
    "span": {
        "color": "white",
        "padding": "14px",
        "font-family": "'Inter', 'Helvetica Neue', sans-serif",
        "font-weight": "500",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "600",
        "padding": "14px",
        "font-family": "'Inter', 'Helvetica Neue', sans-serif",
    }
}

# Remover menu lateral e botão de configurações
options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Definir páginas e link personalizado no lugar do ícone
pages = ["RMC Data", "Documentation", "Examples", "Community", "About"]
urls = {"RMC Data": "#"}  # '#' faz voltar ao topo (página inicial)

# Barra de navegação superior
page = st_navbar(pages, urls=urls, styles=styles, options=options)

# Lógica de conteúdo
if page == "RMC Data":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

    st.markdown(
        "A Região Metropolitana de Campinas foi criada em 2000, através da Lei Complementar nº 870, do estado de São Paulo e é constituída por 20 municípios. "
        "Em 2021, a RMC apresentou um PIB de 266,8 bilhões de reais, o equivalente a 3,07% do Produto Interno Bruto brasileiro no mesmo ano."
    )
    st.markdown(
        "Em 2020, o Instituto Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de Campinas como uma das 15 metrópoles brasileiras."
    )

    # Carregamento dos dados geográficos
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values(by="NM_MUN")

    # Dados socioeconômicos
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

    # Carregar o HTML interativo refinado
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # Substituir o placeholder pelo GeoJSON gerado
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

    # Exibir HTML
    st.components.v1.html(html_code, height=600, scrolling=False)

elif page == "Documentation":
    st.title("📄 Documentation")
    st.write("Aqui você pode colocar a documentação do seu app...")

elif page == "Examples":
    st.title("💡 Examples")
    st.write("Exemplos do app...")

elif page == "Community":
    st.title("👥 Community")
    st.write("Links para a comunidade...")

elif page == "About":
    st.title("ℹ️ About")
    st.write("Sobre o projeto...")
