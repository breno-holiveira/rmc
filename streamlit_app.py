import streamlit as st
import pandas as pd
import geopandas as gpd
import json

st.set_page_config(page_title="RMC Data", layout="wide")

# Remove a barra lateral
st.markdown("""
<style>
div[data-testid="stSidebar"] {display:none !important;}
div[data-testid="stAppViewContainer"] > .main > div:first-child {
    max-width: 100% !important;
    padding-left: 1rem !important;
}

/* Barra horizontal fixa */
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 52px;
    background-color: #ff6600;
    display: flex;
    align-items: center;
    padding: 0 30px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    z-index: 9999;
    box-shadow: 0 4px 8px rgba(255,102,0,0.3);
    user-select: none;
}

/* Itens do menu */
.navbar a {
    color: white;
    text-decoration: none;
    padding: 10px 18px;
    margin: 0 8px;
    border-radius: 8px;
    transition: background-color 0.3s ease;
}

/* Hover */
.navbar a:hover {
    background-color: rgba(255,255,255,0.3);
}

/* Item ativo */
.navbar a.active {
    background-color: #cc5200;
    box-shadow: 0 0 10px #cc5200;
}

/* Espaço para conteúdo */
.content {
    padding-top: 65px;
    max-width: 1200px;
    margin: 0 auto 2rem auto;
}
</style>
""", unsafe_allow_html=True)

# Inicializa a página ativa
if "page" not in st.session_state:
    st.session_state.page = "home"

# Função para atualizar página via clique (usando URL params para funcionar direitinho)
def set_page(page_name):
    st.session_state.page = page_name

# Renderiza a navbar com links clicáveis que atualizam st.session_state.page
# Usando <a href="#"> + onclick JS para evitar reload da página
# E usando Streamlit rerun para atualizar o app

# Criando script JS para alterar o st.session_state.page via streamlit-event
js_script = """
<script>
const links = document.querySelectorAll('.navbar a');
links.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const page = this.getAttribute('data-page');
        // Atualiza query param da URL para paginação via Streamlit rerun
        const searchParams = new URLSearchParams(window.location.search);
        searchParams.set('page', page);
        const newRelativePathQuery = window.location.pathname + '?' + searchParams.toString();
        window.history.pushState(null, '', newRelativePathQuery);
        window.location.reload();
    });
});
</script>
"""

# Atualiza página do Streamlit pelo parâmetro URL
params = st.query_params
page_url = params.get("page", [None])[0]

if page_url:
    st.session_state.page = page_url

# Construir navbar com links ativos e data-page para JS
menu_items = {
    "Início": "home",
    "Página 1": "pag1",
    "Página 2": "pag2",
    "Página 3": "pag3",
}

menu_html = '<div class="navbar">\n'
for label, p in menu_items.items():
    active_class = "active" if st.session_state.page == p else ""
    menu_html += f'<a href="#" class="{active_class}" data-page="{p}">{label}</a>\n'
menu_html += '</div>\n' + js_script

st.markdown(menu_html, unsafe_allow_html=True)

# Conteúdo variável
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

st.markdown('</div>', unsafe_allow_html=True)
