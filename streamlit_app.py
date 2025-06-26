import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

# Remove barra lateral padrão
st.markdown("""
<style>
/* Remove barra lateral do Streamlit */
div[data-testid="stSidebar"] {display:none !important;}
div[data-testid="stAppViewContainer"] > .main > div:first-child {
    max-width: 100% !important;
    padding-left: 1rem !important;
}

/* Barra fixa horizontal */
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 52px;
    background-color: #ff6600;
    display: flex;
    align-items: center;
    padding: 0 30px;
    gap: 1.5rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    z-index: 9999;
    box-shadow: 0 4px 8px rgba(255,102,0,0.3);
    user-select: none;
}
.navbar button {
    background: transparent;
    border: none;
    color: white;
    cursor: pointer;
    padding: 10px 22px;
    border-radius: 12px;
    transition: background-color 0.3s ease;
    font-weight: 700;
    font-size: 1rem;
}
.navbar button:hover {
    background-color: rgba(255,255,255,0.3);
}
.navbar button.active {
    background-color: #cc5200;
    box-shadow: 0 0 10px #cc5200;
}

/* Conteúdo abaixo da navbar */
.content {
    padding-top: 65px;
    max-width: 1200px;
    margin: 0 auto 2rem auto;
}
</style>
""", unsafe_allow_html=True)

# Inicializa a página ativa no estado
if "page" not in st.session_state:
    st.session_state.page = "home"

def nav_button(page_name, label):
    is_active = st.session_state.page == page_name
    css_class = "active" if is_active else ""
    if st.button(label, key=page_name, help=f"Abrir {label}"):
        st.session_state.page = page_name
    # Aplicar classe ativa via JS (ou com css seletor botão pressionado) não possível direto no st.button, 
    # então a cor do botão ativo será controlada pela renderização abaixo

# Barra de navegação customizada via botões (horizontal)
st.markdown('<div class="navbar">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1,1,1,1], gap="large")

with col1:
    if st.button("Início", key="home"):
        st.session_state.page = "home"
with col2:
    if st.button("Página 1", key="pag1"):
        st.session_state.page = "pag1"
with col3:
    if st.button("Página 2", key="pag2"):
        st.session_state.page = "pag2"
with col4:
    if st.button("Página 3", key="pag3"):
        st.session_state.page = "pag3"
st.markdown('</div>', unsafe_allow_html=True)

# Agora corrigir o estilo do botão ativo para os 4 botões (que não é trivial via st.button)

# Conteúdo condicional baseado na página selecionada
st.markdown('<div class="content">', unsafe_allow_html=True)

if st.session_state.page == "home":
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    @st.cache_data
    def carregar_dados():
        gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
        if gdf.crs != 'EPSG:4326':
            gdf = gdf.to_crs('EPSG:4326')
        gdf = gdf.sort_values(by='NM_MUN')

        df = pd.read_excel('dados_rmc.xlsx')
        df.set_index("nome", inplace=True)
        return gdf, df

    @st.cache_resource
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
    st.header("Conteúdo da Página 1")
    st.write("Aqui vai o conteúdo da página 1.")

elif st.session_state.page == "pag2":
    st.header("Conteúdo da Página 2")
    st.write("Aqui vai o conteúdo da página 2.")

elif st.session_state.page == "pag3":
    st.header("Conteúdo da Página 3")
    st.write("Aqui vai o conteúdo da página 3.")

else:
    st.error("Página não encontrada.")

st.markdown("</div>", unsafe_allow_html=True)
