import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import os

def show():

    # Caminhos dos arquivos
    shapefile_path = "./shapefile_rmc/RMC_municipios.shp"
    excel_path = "./dados_rmc.xlsx"
    html_path = "./grafico_rmc.html"

    # Verifica se os arquivos existem
    if not os.path.exists(shapefile_path):
        st.error("Shapefile não encontrado.")
        return
    if not os.path.exists(excel_path):
        st.error("Arquivo de dados .xlsx não encontrado.")
        return
    if not os.path.exists(html_path):
        st.error("Arquivo HTML do mapa não encontrado.")
        return

    # Carregamento dos dados geoespaciais
    gdf = gpd.read_file(shapefile_path)
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    gdf = gdf.sort_values(by='NM_MUN')

    # Carregamento dos dados econômicos
    df = pd.read_excel(excel_path, engine="openpyxl")
    df.set_index("nome", inplace=True)

    # Construção do GeoJSON
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})

    geojson = {"type": "FeatureCollection", "features": features}
    geojson_str = json.dumps(geojson)

    # Leitura do HTML e substituição do placeholder
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read().replace("__GEOJSON_PLACEHOLDER__", geojson_str)

    # Texto explicativo acima do mapa
    st.markdown("### Bem-vindo ao RMC Data")
    st.markdown("### Portal de dados e indicadores da Região Metropolitana de Campinas")
    st.markdown("""
Criada em 2000 pela Lei Complementar nº 870 do Estado de São Paulo, a Região Metropolitana de Campinas é formada por 20 municípios que se destacam pela alta qualidade de vida e desenvolvimento socioeconômico. O RMC Data é uma iniciativa independente que reúne e divulga indicadores econômicos e sociais confiáveis e atualizados sobre a região.

Explore o **mapa interativo** para conhecer os municípios da região:
""")

    # Renderização do HTML do mapa
    st.components.v1.html(html_content, height=500, scrolling=False)

    # Destaques institucionais com fontes discretas

    st.markdown('### Destaques da RMC')

    st.markdown("""
    - Campinas é oficialmente reconhecida como a Capital Nacional da Ciência, Tecnologia e Inovação, conforme o Projeto de Lei nº 3680/2023. [Fonte](https://www.camara.leg.br/propostas-legislativas/2366677)

    - A região possui seis municípios entre os 30 mais seguros do Brasil, com Valinhos ocupando a 1ª posição, segundo dados do IBGE e do Ministério da Saúde. [Fonte](https://tabnet.datasus.gov.br/)

    - Campinas é a única cidade do interior do Brasil com status de metrópole, segundo o IBGE. [Fonte](https://biblioteca.ibge.gov.br/index.php/biblioteca-catalogo?view=detalhes&id=2101728)

    - Em 2025, Campinas foi eleita a melhor cidade do interior para investimentos, de acordo com a *Oxford Economics Global Cities Index*. [Fonte](https://www.oxfordeconomics.com/resource/global-cities-index-2025/)
    """)

    # Informativo de atualização
    st.markdown("##### Última atualização: Junho de 2025")
