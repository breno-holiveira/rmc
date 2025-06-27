import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Importar fonte Inter via Google Fonts para suavidade e legibilidade
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        /* Navbar container */
        .stHorizontalBlock {
            background-color: #1f2937 !important;  /* cinza escuro */
            padding: 0 !important;
            height: 42px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-size: 14px !important;
            letter-spacing: 0.02em !important;
        }

        /* Logo container */
        .navbar-logo {
            display: flex;
            align-items: center;
            margin-left: 16px;
            margin-right: 24px;
            cursor: pointer;
            user-select: none;
            text-decoration: none;
            color: #a3bffa;
            font-weight: 600;
            font-size: 18px;
            transition: color 0.3s ease;
        }
        .navbar-logo:hover {
            color: #7c90f4;
        }
        .navbar-logo img {
            height: 26px;
            width: 26px;
            margin-right: 8px;
        }

        /* Navbar items */
        .stHorizontalBlock span {
            color: rgba(255,255,255,0.85) !important;
            padding: 8px 12px !important;
            margin: 0 6px !important;
            font-weight: 400 !important;
            cursor: pointer;
            user-select: none;
            transition: color 0.2s ease, box-shadow 0.3s ease;
        }
        /* Hover nos itens */
        .stHorizontalBlock span:hover {
            color: #a3bffa !important;
            box-shadow: inset 0 -2px 0 #a3bffa;
        }
        /* Item ativo */
        .stHorizontalBlock [aria-selected="true"] span {
            color: #7c90f4 !important;
            font-weight: 600 !important;
            box-shadow: inset 0 -3px 0 #7c90f4;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "8px 12px",
        "font-weight": "400",
        "font-size": "14px",
        "letter-spacing": "0.02em",
        "cursor": "pointer",
        "user-select": "none",
        "transition": "color 0.2s ease, box-shadow 0.3s ease",
    },
    "active": {
        "color": "#7c90f4",
        "font-weight": "600",
        "box-shadow": "inset 0 -3px 0 #7c90f4",
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = ["Inicio", "Sobre", "Economia", "Finanças Públicas", "Segurança", "População"]

# Definindo o logo_path e link para o GitHub
logo_path = "git.svg"
logo_url = "https://github.com/breno-holiveira/rmc"

# Exibe o navbar com logo e texto customizados
page = st_navbar(
    pages,
    logo_path=logo_path,
    logo_link=logo_url,
    logo_text="RMC Data",
    styles=styles,
    options=options,
)

# Inject custom HTML para o logo + texto no navbar
# Aqui usamos um hack para forçar o clique do logo e texto abrirem link externo
# Essa parte aparece antes da navbar e usa css para posicionar corretamente
st.markdown(f"""
    <style>
    .stHorizontalBlock > div {{
        display: flex !important;
        align-items: center !important;
    }}
    </style>
    <a href="{logo_url}" target="_blank" rel="noopener noreferrer" class="navbar-logo" style="position: absolute; left: 16px; top: 7px; z-index: 9999;">
        <img src="{logo_path}" alt="Logo" />
        RMC Data
    </a>
""", unsafe_allow_html=True)


# Conteúdo da página conforme seleção
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
