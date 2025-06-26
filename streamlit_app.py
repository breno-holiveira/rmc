import streamlit as st
import pandas as pd
import geopandas as gpd
import json

import pages.pag1 as pag1
import pages.pag2 as pag2
import pages.pag3 as pag3

st.set_page_config(page_title="RMC Data", layout="wide")

# Remove barra lateral padrão
st.markdown("""
<style>
div[data-testid="stSidebar"] {display:none !important;}
div[data-testid="stAppViewContainer"] > .main > div:first-child {
    max-width: 100% !important;
    padding-left: 1rem !important;
}
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    background-color: #ff6600;
    padding: 12px 32px;
    display: flex;
    gap: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 700;
    font-size: 16px;
    z-index: 9999;
    box-shadow: 0 4px 8px rgba(255,102,0,0.3);
}
.navbar button {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    padding: 10px 20px;
    border-radius: 10px;
    transition: background-color 0.3s ease;
    font-weight: 700;
}
.navbar button:hover {
    background-color: rgba(255,255,255,0.3);
}
.navbar button.active {
    background-color: #cc5200;
    box-shadow: 0 0 8px #cc5200;
    color: white;
}
.content {
    padding-top: 70px;
    max-width: 1200px;
    margin: 0 auto 40px auto;
}
</style>
""", unsafe_allow_html=True)

# Inicializa página ativa
if "page" not in st.session_state:
    st.session_state.page = "home"

def set_page(page_name):
    st.session_state.page = page_name

# Barra fixa em HTML + JS para trocar página e ativar botão
navbar_html = f"""
<div class="navbar">
    <button id="btn-home" {'class="active"' if st.session_state.page == "home" else ""}>Início</button>
    <button id="btn-pag1" {'class="active"' if st.session_state.page == "pag1" else ""}>Página 1</button>
    <button id="btn-pag2" {'class="active"' if st.session_state.page == "pag2" else ""}>Página 2</button>
    <button id="btn-pag3" {'class="active"' if st.session_state.page == "pag3" else ""}>Página 3</button>
</div>

<script>
const buttons = {{
    "home": document.getElementById("btn-home"),
    "pag1": document.getElementById("btn-pag1"),
    "pag2": document.getElementById("btn-pag2"),
    "pag3": document.getElementById("btn-pag3")
}};

function setActive(page) {{
    for (const key in buttons) {{
        buttons[key].classList.remove("active");
    }}
    buttons[page].classList.add("active");
}}

// Envia evento para Streamlit via window.postMessage
for (const [key, btn] of Object.entries(buttons)) {{
    btn.onclick = () => {{
        window.parent.postMessage({{func: "setPage", page: key}}, "*");
        setActive(key);
    }};
}};
</script>
"""

st.components.v1.html(navbar_html, height=60)

# JS que escuta o postMessage para atualizar st.session_state.page
st.components.v1.html("""
<script>
window.addEventListener("message", (event) => {
    if(event.data.func === "setPage"){
        window.parent.location.href = "?page=" + event.data.page;
    }
});
</script>
""", height=0)

# Atualiza página a partir do query param (parâmetro URL)
page = st.experimental_get_query_params().get("page", ["home"])[0]
if page != st.session_state.page:
    st.session_state.page = page

st.markdown('<div class="content">', unsafe_allow_html=True)

# Conteúdo dinâmico
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
