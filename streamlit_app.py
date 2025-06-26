import streamlit as st
import pandas as pd
import geopandas as gpd
import json

# Configurações iniciais
st.set_page_config(page_title="RMCx Data", layout="wide")

# CSS personalizado
st.markdown("""
<style>
/* Remove header, footer, barra lateral */
header, footer, [data-testid="stSidebar"] {
    display: none !important;
}
.block-container {
    padding-top: 0rem !important;
}

/* Barra de navegação customizada */
.navbar {
    display: flex;
    gap: 24px;
    background-color: #1e2a38;
    padding: 14px 32px;
    border-radius: 0 0 8px 8px;
    position: sticky;
    top: 0;
    z-index: 1000;
}
.navbar button {
    all: unset;
    padding: 8px 16px;
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 500;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.2s ease;
}
.navbar button:hover {
    background-color: #334155;
    color: #ffffff;
}
.navbar button.active {
    background-color: #3b536e;
    color: #ffffff;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# === Barra de navegação ===
abas = ["Início", "PIB por Município", "Indicadores Demográficos", "Comparativo Regional"]
aba_atual = st.session_state.get("aba_atual", "Início")

# Renderiza barra
st.markdown('<div class="navbar">', unsafe_allow_html=True)
for nome in abas:
    ativa = "active" if nome == aba_atual else ""
    if st.button(nome, key=nome):
        st.session_state.aba_atual = nome
st.markdown("</div>", unsafe_allow_html=True)

# Carregamento de dados
@st.cache_data
def carregar_df():
    df = pd.read_excel('dados_rmc.xlsx')
    df.set_index("nome", inplace=True)
    return df

@st.cache_data
def carregar_gdf():
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    return gdf.sort_values(by='NM_MUN')

@st.cache_data
def construir_geojson():
    gdf = carregar_gdf()
    df = carregar_df()
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": props
        })
    return json.dumps({"type": "FeatureCollection", "features": features})

@st.cache_resource
def carregar_html_base():
    with open("grafico_rmc.html", "r", encoding="utf-8") as f:
        return f.read()

# === Conteúdo da aba selecionada ===
aba_atual = st.session_state.get("aba_atual", "Início")

if aba_atual == "Início":
    st.title("RMC Data")
    st.markdown("### Dados e indicadores da Região Metropolitana de Campinas")

    geojson_js = construir_geojson()
    html_template = carregar_html_base()
    html_code = html_template.replace("const geo = __GEOJSON_PLACEHOLDER__;", f"const geo = {geojson_js};")
    st.components.v1.html(html_code, height=600, scrolling=False)

elif aba_atual == "PIB por Município":
    st.header("PIB por Município")
    st.markdown("Visualização detalhada do PIB dos municípios da RMC.")
    st.dataframe(carregar_df()[["PIB (2021)"]])

elif aba_atual == "Indicadores Demográficos":
    st.header("Indicadores Demográficos")
    st.markdown("População, área e densidade demográfica.")
    st.dataframe(carregar_df()[["populacao", "área", "densidade"]])

elif aba_atual == "Comparativo Regional":
    st.header("Comparativo Regional")
    st.markdown("Comparações de indicadores entre os municípios.")
    df = carregar_df()
    st.bar_chart(df["PIB (2021)"].sort_values(ascending=False))
