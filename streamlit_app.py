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
/* Oculta barra lateral padrão */
div[data-testid="stSidebar"] {display:none !important;}
/* Ajusta área principal para ocupar 100% da largura */
div[data-testid="stAppViewContainer"] > .main > div:first-child {
    max-width: 100% !important;
    padding-left: 1rem !important;
}

/* Barra de navegação fixa no topo */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background-color: #ff6600; /* laranja vibrante */
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

/* Espaço para o conteúdo abaixo da navbar */
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

# Renderiza navbar com botões
cols = st.columns([1,1,1,1])
with cols[0]:
    if st.button("Início", key="home_btn", on_click=set_page, args=("home",), 
                 type="primary" if st.session_state.page=="home" else "secondary"):
        pass
with cols[1]:
    if st.button("Página 1", key="pag1_btn", on_click=set_page, args=("pag1",),
                 type="primary" if st.session_state.page=="pag1" else "secondary"):
        pass
with cols[2]:
    if st.button("Página 2", key="pag2_btn", on_click=set_page, args=("pag2",),
                 type="primary" if st.session_state.page=="pag2" else "secondary"):
        pass
with cols[3]:
    if st.button("Página 3", key="pag3_btn", on_click=set_page, args=("pag3",),
                 type="primary" if st.session_state.page=="pag3" else "secondary"):
        pass

# OBS: Como st.button não aceita class styling direto, vamos ajustar o CSS pra "ativar" visual baseado no session_state.
# Porém, botão do Streamlit não suporta class ativa fácil, então vamos usar workaround com javascript abaixo para melhorar.

# Vamos fazer uma navbar custom via HTML + JS pra ativar botão ativo e estética exata laranja:

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

// Envia evento para Streamlit
for (const [key, btn] of Object.entries(buttons)) {{
    btn.onclick = () => {{
        window.parent.postMessage({{func: "setPage", page: key}}, "*");
        setActive(key);
    }};
}}
</script>
"""

st.components.v1.html(navbar_html, height=60)

# Escuta o evento postMessage vindo do JS para trocar a página via streamlit
import streamlit.components.v1 as components

components.html("""
<script>
window.addEventListener("message", (event) => {{
    if (event.data.func === "setPage") {{
        window.parent.location.href = "?page=" + event.data.page;
    }}
}});
</script>
""", height=0)

# Atualiza a página a partir do parâmetro URL (query param)
page = st.experimental_get_query_params().get("page", ["home"])[0]

if page != st.session_state.page:
    st.session_state.page = page

# Espaço para conteúdo
st.markdown('<div class="content">', unsafe_allow_html=True)

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
