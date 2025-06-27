import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Import Google Fonts Inter para garantir a fonte suave
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        /* Aplicar Inter na navbar */
        .stHorizontalBlock span {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-weight: 400 !important;
            font-size: 14px !important;
            letter-spacing: 0.04em !important;
        }
        /* Estilo para item ativo */
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 600 !important;
            background-color: rgba(255,255,255,0.1) !important;
            border-radius: 2px !important;
            padding: 6px 16px !important;
            color: #fff !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }
        /* Espaçamento uniforme para todos os itens */
        .stHorizontalBlock span {
            padding: 6px 16px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.85) !important;
            transition: color 0.3s ease;
        }
        /* Hover suave */
        .stHorizontalBlock span:hover {
            color: #ff7f50 !important;
            cursor: pointer;
        }
        /* Navbar background */
        .stHorizontalBlock {
            background-color: #1f2937 !important;  /* cinza escuro */
            padding: 0 !important;
            height: 40px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

styles = {
    "nav": {
        "background-color": "#1f2937",  # Cinza escuro (funcional, mas o css acima faz o principal)
        "justify-content": "left",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "6px 16px",
        "font-weight": "400",
    },
    "active": {
        "background-color": "rgba(255,255,255,0.1)",
        "color": "#ffffff",
        "font-weight": "600",
        "padding": "6px 16px",
        "border-radius": "2px",
        "border": "1px solid rgba(255,255,255,0.2)",
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = ["Inicio", "Documentation", "Examples", "Community", "About"]

page = st_navbar(pages, styles=styles, options=options)

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
