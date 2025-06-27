import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Importa fonte Inter
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
/* Estilo para a navbar do pacote */
[data-testid="stHorizontalBlock"] > div:first-child {
    background-color: #1f2937;
    display: flex;
    align-items: center;
    padding: 0 1.5rem;
    height: 48px;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15);
    user-select: none;
    gap: 1rem;
}

/* Container do logo + texto (estilo custom, fora do pacote) */
#custom-logo {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #a3bffa;
    font-weight: 600;
    font-size: 18px;
    cursor: pointer;
    flex-shrink: 0;
    text-decoration: none;
    transition: color 0.3s ease;
}
#custom-logo:hover {
    color: #7c90f4;
}
#custom-logo img {
    height: 28px;
    width: 28px;
    object-fit: contain;
}

/* Ajusta container dos itens do menu */
[data-testid="stHorizontalBlock"] > div:first-child > div:nth-child(2) {
    display: flex !important;
    justify-content: center;
    flex-grow: 1;
    gap: 1rem;
    font-size: 14px;
}

/* Itens do menu */
[data-testid="stHorizontalBlock"] button, 
[data-testid="stHorizontalBlock"] div[role="tab"] {
    color: rgba(255,255,255,0.85);
    background-color: transparent;
    border: none;
    padding: 6px 12px;
    border-radius: 6px;
    font-weight: 400;
    transition: background-color 0.2s ease, color 0.2s ease;
    cursor: pointer;
    min-width: 80px;
}
[data-testid="stHorizontalBlock"] button:hover,
[data-testid="stHorizontalBlock"] div[role="tab"]:hover {
    color: #a3bffa;
    background-color: rgba(163,191,250,0.15);
}
[data-testid="stHorizontalBlock"] button[aria-selected="true"],
[data-testid="stHorizontalBlock"] div[role="tab"][aria-selected="true"] {
    color: #7c90f4;
    background-color: rgba(124,144,244,0.2);
    font-weight: 600;
}

/* Remove outline azul ao focar */
[data-testid="stHorizontalBlock"] button:focus,
[data-testid="stHorizontalBlock"] div[role="tab"]:focus {
    outline: none;
}
</style>
""", unsafe_allow_html=True)

# Páginas do menu
pages = ["Inicio", "Sobre", "Economia", "Finanças Públicas", "Segurança", "População"]

# Renderiza a navbar e captura a aba selecionada
page = st_navbar(
    pages,
    styles={
        "nav": {
            "background-color": "transparent",  # usamos cor no CSS custom acima
            "justify-content": "center",  # centraliza os itens do menu
            "font-family": "'Inter', sans-serif",
            "font-size": "14px",
        },
        "span": {
            "color": "rgba(255,255,255,0.85)",
            "padding": "6px 12px",
            "font-weight": "400",
            "border-radius": "6px",
        },
        "active": {
            "color": "#7c90f4",
            "background-color": "rgba(124,144,244,0.2)",
            "font-weight": "600",
            "border-radius": "6px",
        },
    },
    options={
        "show_menu": False,
        "show_sidebar": False,
    }
)

# Logo + texto manual na barra, injetado acima da navbar
st.markdown("""
    <a id="custom-logo" href="/" >
        <img src="cubes.svg" alt="Logo Cubes" />
        RMC Data
    </a>
""", unsafe_allow_html=True)

# Conteúdo das páginas
if page == "Inicio":
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

elif page == "Sobre":
    st.title("Sobre")
    st.write("Conteúdo sobre o projeto e informações institucionais.")

elif page == "Economia":
    st.title("Economia")
    st.write("Indicadores e análises econômicas da região.")

elif page == "Finanças Públicas":
    st.title("Finanças Públicas")
    st.write("Informações e dados sobre finanças públicas locais.")

elif page == "Segurança":
    st.title("Segurança")
    st.write("Estatísticas e análises sobre segurança pública.")

elif page == "População":
    st.title("População")
    st.write("Dados demográficos e análises populacionais.")
