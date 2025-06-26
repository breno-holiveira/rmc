import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_community_navigation_bar import st_navbar  # Import correto

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Barra de navegação (obrigatoriamente logo após o set_page_config)
page = st_navbar(
    ["Home", "Documentação", "Exemplos", "Sobre"],
    options={"use_padding": False}
)

# Página principal: HOME
if page == "Home":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")

    st.markdown("""
    A Região Metropolitana de Campinas foi criada em 2000, através da [Lei Complementar nº 870](https://www.al.sp.gov.br/repositorio/legislacao/lei.complementar/2000/lei.complementar-870-19.06.2000.html), 
    e é constituída por 20 municípios. Em 2021, a RMC apresentou um PIB de **R$ 266,8 bilhões**, o equivalente a **3,07%** do Produto Interno Bruto brasileiro no mesmo ano.

    Em 2020, o Instituto Brasileiro de Geografia e Estatística (IBGE) classificou a cidade de Campinas como uma das 15 metrópoles brasileiras.
    """)

    # Carregamento de dados geográficos
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    gdf = gdf.sort_values(by='NM_MUN')

    # Carregamento de dados estatísticos
    df = pd.read_excel('dados_rmc.xlsx')
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

    # Leitura do HTML externo refinado
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # Inserção do GeoJSON dentro do HTML
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

    # Exibição do gráfico interativo na página
    st.components.v1.html(html_code, height=600, scrolling=False)

# Página: Documentação
elif page == "Documentação":
    st.title("📚 Documentação")
    st.markdown("A documentação será disponibilizada em breve.")

# Página: Exemplos
elif page == "Exemplos":
    st.title("🔍 Exemplos")
    st.markdown("Aqui serão apresentados exemplos de visualizações e comparações municipais.")

# Página: Sobre
elif page == "Sobre":
    st.title("ℹ️ Sobre o Projeto")
    st.markdown("""
    Desenvolvido por **Breno Oliveira**  
    Dados fornecidos por: IBGE, SEADE, CONFEA  
    Última atualização: 2025

    [GitHub do projeto](https://github.com/breno) (exemplo)
    """)
