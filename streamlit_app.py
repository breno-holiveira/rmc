import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# Definição do estilo personalizado seguindo a doc oficial
style = {
    "txColor": "#f0f0f0",            # Cor do texto
    "txColorHover": "#ff7200",       # Cor do texto ao passar mouse
    "bgColor": "#0d1f3c",            # Cor de fundo da navbar
    "bgColorHover": "#163466",       # Fundo do item ao passar mouse
    "bgColorActive": "#ff7200",      # Fundo do item ativo
    "txColorActive": "#ffffff",      # Texto do item ativo
    "height": 50,                    # Altura da navbar em px
    "font": "Roboto, sans-serif",    # Fonte customizada
    "fontWeight": "600",             # Peso da fonte
    "iconName": "📊",                # Ícone no lado esquerdo
    "iconSize": 25,                  # Tamanho do ícone
    "iconColor": "#ff7200",          # Cor do ícone
    "iconColorActive": "#ffffff",    # Cor do ícone ativo (mesma do texto ativo)
}

# Barra de navegação com estilo aplicado
page = st_navbar(
    options=["Home", "Documentation", "Examples", "Community", "About"],
    style=style
)

# Conteúdo conforme aba selecionada
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

    # Carregar HTML externo refinado (seu gráfico)
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # Substituir placeholder pelo GeoJSON gerado
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

    # Exibir HTML no Streamlit
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
