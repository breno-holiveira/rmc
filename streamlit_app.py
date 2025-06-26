import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Configuração da página
st.set_page_config(page_title="RMCs Data", layout="wide", page_icon="📊")

# CSS personalizado para estilizar a barra de navegação do streamlit_navigation_bar
custom_css = """
<style>
/* Container da navbar */
[data-testid="stHorizontalBlock"] > div:first-child {
    background: linear-gradient(90deg, #0d1f3c, #163466);
    padding: 0.6rem 1rem;
    font-family: 'Roboto', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    color: white;
    border-radius: 0 0 15px 15px;
    position: sticky;
    top: 0;
    z-index: 9999;
    box-shadow: 0 3px 8px rgb(0 0 0 / 0.3);
}

/* Itens da navbar */
[data-testid="stHorizontalBlock"] button, 
[data-testid="stHorizontalBlock"] div[role="tab"] {
    color: white;
    background-color: transparent;
    border: none;
    margin: 0 12px;
    padding: 6px 14px;
    border-radius: 8px;
    transition: background-color 0.3s ease, color 0.3s ease;
    cursor: pointer;
}

/* Hover nos itens */
[data-testid="stHorizontalBlock"] button:hover,
[data-testid="stHorizontalBlock"] div[role="tab"]:hover {
    background-color: #ff7200;
    color: #fff9f0;
}

/* Item ativo */
[data-testid="stHorizontalBlock"] button[aria-selected="true"],
[data-testid="stHorizontalBlock"] div[role="tab"][aria-selected="true"] {
    background-color: #ff7200;
    color: white;
    font-weight: 700;
    box-shadow: 0 0 8px 1px #ff7f27;
}

/* Remover outline ao focar */
[data-testid="stHorizontalBlock"] button:focus,
[data-testid="stHorizontalBlock"] div[role="tab"]:focus {
    outline: none;
}

/* Ajuste do container dos botões para centralizar */
[data-testid="stHorizontalBlock"] > div {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Barra de navegação superior com estilo customizado
page = st_navbar(["Home", "Documentation", "Examples", "Community", "About"])

# Componente retorna a aba selecionada como string
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
