import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# Estilo customizado mais compacto e elegante
styles = {
    "nav": {
        "background-color": "royalblue",
        "justify-content": "left",
        "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-size": "14px",       # fonte menor e mais compacta
        "padding": "0 12px",       # menos espaçamento horizontal
        "height": "48px",          # navbar mais baixa
        "align-items": "center",
    },
    "span": {
        "color": "white",
        "padding": "8px 12px",     # botões com padding reduzido
        "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-weight": "500",
        "transition": "color 0.25s ease, background-color 0.25s ease",
    },
    "active": {
        "background-color": "white",
        "color": "royalblue",
        "font-weight": "600",
        "padding": "8px 12px",
        "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "box-shadow": "0 2px 6px rgba(0,0,0,0.2)",
        "border-radius": "6px",
        "transition": "color 0.25s ease, background-color 0.25s ease",
    },
    "img": {
        "display": "none",  # ocultar logo, pois você quer texto
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Definir páginas
pages = ["Início", "Documentation", "Examples", "Community", "About"]

# URLs para as abas — deixamos vazio para "Início" manter na mesma página
urls = {
    "Início": "#",           # Mantém na mesma página ao clicar
    "Documentation": "",
    "Examples": "",
    "Community": "",
    "About": ""
}

# Barra de navegação customizada
page = st_navbar(pages, urls=urls, styles=styles, options=options)

# Conteúdo da página
if page == "Início":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

    st.markdown(
        "A Região Metropolitana de Campinas foi criada em 2000, através da Lei Complementar nº 870, do estado de São Paulo e é constituída por 20 municípios. "
        "Em 2021, a RMC apresentou um PIB de 266,8 bilhões de reais, o equivalente a 3,07% do Produto Interno Bruto brasileiro no mesmo ano."
    )
    st.markdown(
        "Em 2020, o Instituto Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de Campinas como uma das 15 metrópoles brasileiras."
    )

    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values(by="NM_MUN")

    df = pd.read_excel("dados_rmc.xlsx")
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
