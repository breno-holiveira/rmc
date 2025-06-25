import streamlit as st
import pandas as pd
import geopandas as gpd
import json

import pages.pag1 as pag1
import pages.pag2 as pag2
import pages.pag3 as pag3

st.set_page_config(page_title="RMC Data", layout="wide")

# Remove sidebar completamente
st.markdown("""
<style>
div[data-testid="stSidebar"] {display:none !important;}
div[data-testid="stAppViewContainer"] > .main > div:first-child {
    max-width: 100% !important;
    padding-left: 1rem !important;
}
/* Menu fixo no topo */
.menu-fixed {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    background: rgba(30, 41, 59, 0.85); /* glass azul escuro transparente */
    backdrop-filter: saturate(180%) blur(10px);
    display: flex;
    gap: 24px;
    padding: 14px 32px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 600;
    font-size: 16px;
    color: #cbd5e1;
    border-bottom: 1px solid rgba(100, 116, 139, 0.4);
}
.menu-fixed button {
    background: none;
    border: none;
    color: #cbd5e1;
    cursor: pointer;
    padding: 8px 18px;
    border-radius: 8px;
    transition: background-color 0.25s ease;
    font-weight: 600;
}
.menu-fixed button:hover {
    background-color: #2563eb;
    color: white;
}
.menu-fixed button.active {
    background-color: #1d4ed8;
    color: white;
}
.content-area {
    padding-top: 64px; /* espaço para o menu fixo */
    max-width: 1200px;
    margin: 0 auto 3rem auto;
}
</style>
""", unsafe_allow_html=True)

# Menu fixo no topo
menu_html = """
<div class="menu-fixed">
    <button id="btn-home">Início</button>
    <button id="btn-pag1">Página 1</button>
    <button id="btn-pag2">Página 2</button>
    <button id="btn-pag3">Página 3</button>
</div>

<script>
const buttons = {
    "home": document.getElementById("btn-home"),
    "pag1": document.getElementById("btn-pag1"),
    "pag2": document.getElementById("btn-pag2"),
    "pag3": document.getElementById("btn-pag3")
};
function updateActive(page) {
    for (const key in buttons) {
        buttons[key].classList.remove("active");
    }
    if (buttons[page]) buttons[page].classList.add("active");
}
updateActive("home");

// Escuta os cliques e dispara evento para Streamlit
for (const [key, btn] of Object.entries(buttons)) {
    btn.onclick = () => {
        window.dispatchEvent(new CustomEvent("setPage", {detail: key}));
        updateActive(key);
    };
}
</script>
"""

st.components.v1.html(menu_html, height=60)

# Usar st.query_params para pegar parâmetro page da URL
params = st.query_params
page_param = params.get("page", ["home"])[0]

if "page" not in st.session_state:
    st.session_state.page = "home"

if page_param != st.session_state.page:
    st.session_state.page = page_param

# Atualiza URL com o parâmetro page
def update_query_params(p):
    if st.query_params.get("page", [""])[0] != p:
        st.experimental_set_query_params(page=p)

update_query_params(st.session_state.page)

st.markdown('<div class="content-area">', unsafe_allow_html=True)

if st.session_state.page == "home":
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    @st.cache_data(show_spinner=False)
    def carregar_dados():
        gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
        if gdf.crs != 'EPSG:4326':
            gdf = gdf.to_crs('EPSG:4326')
        gdf = gdf.sort_values(by='NM_MUN')

        df = pd.read_excel('dados_rmc.xlsx')
        df.set_index("nome", inplace=True)
        return gdf, df

    @st.cache_resource(show_spinner=False)
    def carregar_html():
        with open("grafico_rmc.html", "r", encoding="utf-8") as f:
            return f.read()

    gdf, df = carregar_dados()
    html_template = carregar_html()

    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})

    geojson_js = json.dumps({"type": "FeatureCollection", "features": features})
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")

    st.components.v1.html(html_code, height=600, scrolling=False)

elif st.session_state.page == "pag1":
    pag1.main()

elif st.session_state.page == "pag2":
    pag2.main()

elif st.session_state.page == "pag3":
    pag3.main()

else:
    st.error("Página não encontrada.")

st.markdown("</div>", unsafe_allow_html=True)
