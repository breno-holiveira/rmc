import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Fonte Inter via Google Fonts para suavidade e legibilidade
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        /* Navbar container */
        .stHorizontalBlock {
            background-color: #1f2937 !important;
            padding: 0 12px !important;
            height: 44px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important; /* espaço entre logo e GitHub */
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-size: 14px !important;
            letter-spacing: 0.02em !important;
            position: relative;
        }

        /* Logo + texto à esquerda */
        .navbar-left {
            display: flex;
            align-items: center;
            cursor: pointer;
            user-select: none;
            color: #a3bffa;
            font-weight: 600;
            font-size: 18px;
            letter-spacing: 0.03em;
            gap: 8px;
            flex-shrink: 0;
            text-decoration: none;
            transition: color 0.3s ease;
            padding-left: 8px;
        }
        .navbar-left:hover {
            color: #7c90f4;
        }
        .navbar-left img {
            height: 28px;
            width: 28px;
            object-fit: contain;
        }

        /* Itens da navbar central */
        .navbar-center {
            flex-grow: 1;
            display: flex !important;
            justify-content: center !important;
            gap: 8px !important; /* espaçamento entre opções */
        }
        .navbar-center span {
            color: rgba(255,255,255,0.85) !important;
            padding: 8px 14px !important;
            margin: 0 !important;
            font-weight: 400 !important;
            cursor: pointer;
            user-select: none;
            border-radius: 4px;
            transition: color 0.2s ease, background-color 0.2s ease;
        }
        .navbar-center span:hover {
            color: #a3bffa !important;
            background-color: rgba(163, 191, 250, 0.1) !important;
        }
        .navbar-center [aria-selected="true"] span {
            color: #7c90f4 !important;
            font-weight: 600 !important;
            background-color: rgba(124, 144, 244, 0.15) !important;
        }

        /* GitHub no canto direito */
        .navbar-right {
            display: flex;
            align-items: center;
            flex-shrink: 0;
            gap: 12px;
        }
        .navbar-right a {
            color: #a3bffa;
            text-decoration: none;
            display: flex;
            align-items: center;
            transition: color 0.3s ease;
        }
        .navbar-right a:hover {
            color: #7c90f4;
        }
        .navbar-right img {
            height: 24px;
            width: 24px;
            object-fit: contain;
        }

        /* Ajuste para a barra central, deixando espaço para esquerda e direita */
        .stHorizontalBlock > div:nth-child(2) {
            flex-grow: 1;
            justify-content: center !important;
            gap: 8px !important;
            margin: 0 150px; /* deixa espaço para logo e github */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "center",
        "padding": "0 150px",  # Espaço para logo à esquerda e GitHub à direita
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "8px 14px",
        "font-weight": "400",
        "font-size": "14px",
        "letter-spacing": "0.02em",
        "cursor": "pointer",
        "user-select": "none",
        "border-radius": "4px",
        "transition": "color 0.2s ease, background-color 0.2s ease",
        "margin": "0 4px",
    },
    "active": {
        "color": "#7c90f4",
        "font-weight": "600",
        "background-color": "rgba(124, 144, 244, 0.15)",
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = ["Inicio", "Sobre", "Economia", "Finanças Públicas", "Segurança", "População"]

# Barra de navegação principal, mas o logo e GitHub serão custom com CSS
page = st_navbar(pages, styles=styles, options=options)

# --- Logo + texto clicável no canto esquerdo ---
st.markdown(
    """
    <a href="https://github.com/breno-holiveira/rmc" target="_blank" rel="noopener noreferrer" class="navbar-left">
        <img src="cubes.svg" alt="Cubos Logo" />
        RMC Data
    </a>
    """,
    unsafe_allow_html=True,
)

# --- Ícone GitHub no canto direito ---
st.markdown(
    """
    <div class="navbar-right">
        <a href="https://github.com/breno-holiveira/rmc" target="_blank" rel="noopener noreferrer" title="GitHub Repository">
            <img src="git.svg" alt="GitHub Logo" />
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

# === Conteúdo das páginas ===
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
