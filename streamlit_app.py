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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet" />
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
            font-size: 15px !important;
            letter-spacing: 0em !important;
            padding: 6px 8px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.85) !important;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: relative;
            transition: color 0.15s ease, background-color 0.15s ease;
        }
        /* Hover suave para itens */
        .stHorizontalBlock span:hover {
            color: #ff9e3b !important;
        }

        /* Destaque do item ativo: fundo branco sutil e linha laranja */
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 500 !important;
            color: rgba(255,255,255,0.95) !important;
            background-color: rgba(255, 255, 255, 0.12) !important;
            border-radius: 6px;
            padding-left: 12px !important;
            padding-right: 12px !important;
        }
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: '';
            position: absolute;
            left: 10%;
            bottom: 0;
            height: 2px;
            width: 80%;
            background-color: #ff9e3b;
            border-radius: 3px;
        }

        /* Estilo fixo para RMC Data: negrito e sempre cor branca */
        /* O item com texto exato 'RMC Data' */
        .stHorizontalBlock span:has-text("RMC Data") {
            font-weight: 700 !important;
            color: white !important;
            padding-left: 12px !important;
            padding-right: 12px !important;
        }

        /* Quando RMC Data estiver selecionado, só adiciona fundo branco sutil e linha */
        .stHorizontalBlock [aria-selected="true"] span:has-text("RMC Data") {
            background-color: rgba(255, 255, 255, 0.15) !important;
            color: white !important;
            font-weight: 700 !important;
        }
        /* Esconder o underline padrão para RMC Data */
        .stHorizontalBlock [aria-selected="true"] span:has-text("RMC Data")::after {
            background-color: transparent !important;
        }

        /* Logo cubes.svg inline no menu (com margem direita) */
        .stHorizontalBlock span:has-text("RMC Data") {
            display: flex !important;
            align-items: center;
        }
        .stHorizontalBlock span:has-text("RMC Data") img {
            height: 22px;
            margin-right: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Para logo inline SVG no menu
# Leitura do svg para inserir inline no menu
with open(logo_path, "r", encoding="utf-8") as f:
    svg_logo = f.read()
# Remover quebras e aspas para inline funcionar dentro do span
svg_logo_inline = svg_logo.replace('\n', '').replace('"', "'").replace('<svg ', '<svg style="height:22px; margin-right:8px;" ')

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
        "font-family": "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-size": "15px",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "6px 8px",
        "font-weight": "400",
        "font-size": "15px",
        "letter-spacing": "0em",
        "margin": "0 6px",
        "white-space": "nowrap",
        "position": "relative",
        "display": "inline-flex",
        "align-items": "center",
    },
    "active": {
        "color": "rgba(255,255,255,0.95)",
        "font-weight": "500",
        "background-color": "rgba(255,255,255,0.12)",
        "border-radius": "6px",
        "padding-left": "12px",
        "padding-right": "12px",
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

# Substituir o texto RMC Data pelo texto + SVG logo no menu (via hack no nome)
# A streamlit_navigation_bar não tem API para inserir logo do lado do texto, então vamos substituir o texto "RMC Data" pelo SVG + texto com HTML no CSS

# Como a navbar apenas recebe texto simples, vamos aproveitar um truque: setar o texto do botão como um caractere especial invisível + o texto real que será substituído via CSS
# Para facilitar, vamos usar um caractere invisível no nome e usar CSS para mostrar o SVG + texto real

# Porém, para simplicidade aqui, vamos usar um patch simples: depois que a navbar renderizar, substituir via JS

# Vamos montar o menu normalmente e injetar um script para substituir o texto do primeiro item ("RMC Data") pelo SVG inline + texto

page = st_navbar(pages, styles=styles, options=options)

# Inject JS para alterar texto do primeiro item da navbar e adicionar SVG
js_code = f"""
<script>
    const navItems = document.querySelectorAll('.stHorizontalBlock span');
    if(navItems.length > 0) {{
        const firstItem = navItems[0];
        firstItem.innerHTML = `{svg_logo_inline} RMC Data`;
        firstItem.style.fontWeight = '700';
        firstItem.style.color = 'white';
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
