import os
import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Caminho para cubes.svg
logo_path = os.path.join(os.getcwd(), "cubes.svg")

# Importa fonte Inter
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet" />
    <style>
        /* Container navbar */
        .stHorizontalBlock {
            background-color: #1f2937 !important; /* cinza escuro */
            padding: 0 !important;
            height: 44px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
            user-select: none;
        }

        /* Itens da navbar */
        .stHorizontalBlock span {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-weight: 400 !important;
            font-size: 14px !important;
            letter-spacing: 0em !important;
            padding: 6px 8px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.85) !important;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: relative;
            transition: color 0.2s ease;
            display: inline-flex !important;
            align-items: center !important;
        }

        /* Hover suave */
        .stHorizontalBlock span:hover {
            color: #7dd3fc !important;  /* Azul claro */
        }

        /* Item ativo: só muda cor da fonte */
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 600 !important;
            color: #3b82f6 !important;  /* Azul sutil para ativo */
            background-color: transparent !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            padding-left: 8px !important;
            padding-right: 8px !important;
        }

        /* Remove underline ou qualquer ::after no item ativo */
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: none !important;
        }

        /* RMC Data sempre em negrito e cor diferente */
        .stHorizontalBlock span:has-text("RMC Data") {
            font-weight: 700 !important;
            color: #60a5fa !important; /* Azul claro e discreto */
            padding-left: 10px !important;
            padding-right: 10px !important;
        }

        /* RMC Data ativo: mantém negrito, só muda a cor para um azul mais forte */
        .stHorizontalBlock [aria-selected="true"] span:has-text("RMC Data") {
            color: #2563eb !important;
            font-weight: 700 !important;
            background-color: transparent !important;
        }

        /* Ajustar tamanho do logo inline SVG e margem */
        .stHorizontalBlock span:has-text("RMC Data") svg {
            height: 20px !important;
            margin-right: 6px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Preparar SVG para inline no menu
with open(logo_path, "r", encoding="utf-8") as f:
    svg_logo = f.read()
svg_logo_inline = svg_logo.replace('\n', '').replace('"', "'").replace('<svg ', '<svg style="height:20px; margin-right:6px;" ')

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
        "font-family": "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-size": "14px",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "6px 8px",
        "font-weight": "400",
        "font-size": "14px",
        "letter-spacing": "0em",
        "margin": "0 6px",
        "white-space": "nowrap",
        "position": "relative",
        "display": "inline-flex",
        "align-items": "center",
    },
    "active": {
        "color": "#3b82f6",
        "font-weight": "600",
        "background-color": "transparent",
        "padding-left": "8px",
        "padding-right": "8px",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = [
    "RMC Data",
    "Sobre",
    "Economia",
    "Finanças Públicas",
    "Segurança",
    "População",
]

page = st_navbar(pages, logo_path=logo_path, styles=styles, options=options)

# JS para substituir texto do primeiro item por SVG + texto
js_code = f"""
<script>
    const navItems = document.querySelectorAll('.stHorizontalBlock span');
    if(navItems.length > 0) {{
        const firstItem = navItems[0];
        firstItem.innerHTML = `{svg_logo_inline} RMC Data`;
        firstItem.style.fontWeight = '700';
        firstItem.style.color = '#60a5fa';
        firstItem.style.paddingLeft = '10px';
        firstItem.style.paddingRight = '10px';
    }}
</script>
"""
st.markdown(js_code, unsafe_allow_html=True)

# Conteúdo das páginas

if page == "RMC Data":
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
    st.write("Informações institucionais e gerais sobre o projeto.")

elif page == "Economia":
    st.title("Economia")
    st.write("Conteúdo relacionado à economia da RMC.")

elif page == "Finanças Públicas":
    st.title("Finanças Públicas")
    st.write("Informações sobre finanças públicas da região.")

elif page == "Segurança":
    st.title("Segurança")
    st.write("Dados e análises sobre segurança.")

elif page == "População":
    st.title("População")
    st.write("Indicadores populacionais da Região Metropolitana de Campinas.")
