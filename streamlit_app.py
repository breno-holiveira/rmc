import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# Estilo mais compacto e suave
styles = {
    "nav": {
        "background-color": "#3b5998",  # azul suave, menos vibrante que royalblue
        "justify-content": "left",
        "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-size": "13px",         # fonte menor para evitar "esticado"
        "padding": "0 8px",          # padding horizontal reduzido
        "height": "42px",            # navbar mais baixa
        "align-items": "center",
        "box-shadow": "0 2px 4px rgba(0,0,0,0.12)",
    },
    "span": {
        "color": "white",
        "padding": "6px 10px",       # botões mais compactos
        "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-weight": "500",
        "border-radius": "6px",
        "transition": "background-color 0.3s ease, color 0.3s ease",
        "cursor": "pointer",
        "user-select": "none",
    },
    "span:hover": {
        "background-color": "#2d4373",
        "color": "#e2e6ea",
    },
    "active": {
        "background-color": "white",
        "color": "#3b5998",
        "font-weight": "600",
        "padding": "6px 10px",
        "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "box-shadow": "0 2px 8px rgba(0,0,0,0.15)",
        "border-radius": "6px",
        "cursor": "default",
    },
    "img": {
        "display": "none",  # ocultar logo
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
    "open_new_tab": False,  # garantir que não abre em nova aba
}

# Definir páginas
pages = ["Início", "Documentation", "Examples", "Community", "About"]

# URLs vazias para manter tudo na mesma página
urls = {page: "" for page in pages}

# Barra de navegação
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
