import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Fonte Inter importada para suavidade e legibilidade
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
/* Barra completa */
#custom-navbar {
    position: sticky;
    top: 0;
    z-index: 9999;
    background-color: #1f2937;
    height: 48px;
    display: flex;
    align-items: center;
    padding: 0 20px;
    font-family: 'Inter', sans-serif;
    user-select: none;
    box-shadow: 0 1px 4px rgba(0,0,0,0.15);
}

/* Logo esquerdo */
#custom-logo {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #a3bffa;
    font-weight: 600;
    font-size: 18px;
    cursor: pointer;
    text-decoration: none;
    flex-shrink: 0;
    transition: color 0.3s ease;
}
#custom-logo:hover {
    color: #7c90f4;
}
#custom-logo img {
    height: 28px;
    width: 28px;
    object-fit: contain;
}

/* Menu central */
#custom-menu {
    display: flex;
    flex-grow: 1;
    justify-content: center;
    gap: 12px;
    font-size: 14px;
}

/* Itens do menu */
#custom-menu span {
    color: rgba(255,255,255,0.85);
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease, color 0.2s ease;
}
#custom-menu span:hover {
    color: #a3bffa;
    background-color: rgba(163, 191, 250, 0.1);
}
#custom-menu span.selected {
    font-weight: 600;
    color: #7c90f4;
    background-color: rgba(124, 144, 244, 0.15);
}

/* GitHub direito */
#custom-github {
    flex-shrink: 0;
}
#custom-github a {
    display: flex;
    align-items: center;
    color: #a3bffa;
    text-decoration: none;
    transition: color 0.3s ease;
}
#custom-github a:hover {
    color: #7c90f4;
}
#custom-github img {
    height: 24px;
    width: 24px;
    object-fit: contain;
}
</style>
""", unsafe_allow_html=True)

# Páginas/menu
pages = ["Inicio", "Sobre", "Economia", "Finanças Públicas", "Segurança", "População"]

# Função para renderizar a navbar personalizada
def render_navbar(selected):
    st.markdown(f"""
    <div id="custom-navbar">
        <a id="custom-logo" href="/" onclick="window.location.href='/'">
            <img src="cubes.svg" alt="Logo Cubes"/>
            RMC Data
        </a>
        <div id="custom-menu">
            {"".join(
                [f'<span class="{"selected" if p==selected else ""}" onclick="window.dispatchEvent(new CustomEvent(\'selectPage\', {{detail: \'{p}\'}}))">{p}</span>'
                 for p in pages]
            )}
        </div>
        <div id="custom-github">
            <a href="https://github.com/breno-holiveira/rmc" target="_blank" rel="noopener noreferrer" title="GitHub">
                <img src="git.svg" alt="GitHub"/>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Estado para página selecionada
if 'page' not in st.session_state:
    st.session_state.page = "Inicio"

# Renderiza navbar
render_navbar(st.session_state.page)

# Captura clique via JS e altera estado da página no Streamlit
js = """
<script>
window.addEventListener('selectPage', e => {
    const page = e.detail;
    window.parent.postMessage({isStreamlitMessage: true, type: "streamlit:setComponentValue", value: page}, "*");
});
</script>
"""
st.components.v1.html(js, height=0, width=0)

# Pega o valor da página atual do componente JS
page = st.experimental_get_query_params().get("page", [st.session_state.page])[0]

# Atualiza session_state se mudou
if page != st.session_state.page:
    st.session_state.page = page

# Conteúdo das páginas
if st.session_state.page == "Inicio":
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

elif st.session_state.page == "Sobre":
    st.title("Sobre")
    st.write("Conteúdo sobre o projeto e informações institucionais.")

elif st.session_state.page == "Economia":
    st.title("Economia")
    st.write("Indicadores e análises econômicas da região.")

elif st.session_state.page == "Finanças Públicas":
    st.title("Finanças Públicas")
    st.write("Informações e dados sobre finanças públicas locais.")

elif st.session_state.page == "Segurança":
    st.title("Segurança")
    st.write("Estatísticas e análises sobre segurança pública.")

elif st.session_state.page == "População":
    st.title("População")
    st.write("Dados demográficos e análises populacionais.")
