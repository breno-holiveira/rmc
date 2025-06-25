import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import folium

# Configurações da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    page_icon="📍",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    section[data-testid="stSidebar"] {
        width: 300px !important;
    }
    div.stSelectbox > div > div > div > div {
        color: #1a2d5a;
    }
    div[data-baseweb="select"] > div {
        border-color: #4d648d !important;
    }
    .metric-box {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stPlotlyChart {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Título e descrição
st.title("📊 RMC Data")
st.markdown("### Análise dos dados e indicadores da Região Metropolitana de Campinas")

# Carregamento dos dados
@st.cache_data
def load_data():
    gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
    if gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    gdf = gdf.sort_values(by='NM_MUN')
    
    df = pd.read_excel('dados_rmc.xlsx')
    df.set_index("nome", inplace=True)
    
    # Construção do GeoJSON com dados
    features = []
    for _, row in gdf.iterrows():
        nome = row["NM_MUN"]
        geom = row["geometry"].__geo_interface__
        props = df.loc[nome].to_dict() if nome in df.index else {}
        props["name"] = nome
        features.append({"type": "Feature", "geometry": geom, "properties": props})
    
    return {"type": "FeatureCollection", "features": features}, df

geojson, df = load_data()
geojson_str = json.dumps(geojson)

# Sidebar - Filtros e seleções
with st.sidebar:
    st.subheader("🔍 Filtros")
    selected_municipio = st.selectbox(
        "Selecione um município",
        df.index,
        index=0
    )
    
    st.subheader("📊 Opções de Visualização")
    show_map = st.checkbox("Mostrar mapa interativo", value=True)
    show_graphs = st.checkbox("Mostrar gráficos comparativos", value=True)
    
    st.markdown("---")
    st.markdown("ℹ️ **Sobre os dados**")
    st.caption("Fonte: IBGE Cidades e outras fontes oficiais")

# Seção principal
tab1, tab2 = st.tabs(["📌 Visão Geral", "📈 Análise Detalhada"])

with tab1:
    # Cartões de métricas para o município selecionado
    if selected_municipio in df.index:
        m_data = df.loc[selected_municipio]
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="metric-box">
                    <h3 style='margin:0;color:#4d648d'>PIB 2021</h3>
                    <p style='font-size:24px;font-weight:bold;margin:5px 0;'>R$ {}</p>
                </div>
            """.format(f"{m_data.get('pib_2021', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
            unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
                <div class="metric-box">
                    <h3 style='margin:0;color:#4d648d'>População (2022)</h3>
                    <p style='font-size:24px;font-weight:bold;margin:5px 0;'>{:,}</p>
                </div>
            """.format(m_data.get('populacao_2022', 0)).replace(",", "."),
            unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
                <div class="metric-box">
                    <h3 style='margin:0;color:#4d648d'>PIB per capita</h3>
                    <p style='font-size:24px;font-weight:bold;margin:5px 0;'>R$ {}</p>
                </div>
            """.format(f"{m_data.get('per_capita_2021', 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
            unsafe_allow_html=True)

    # Mapa interativo
    if show_map:
        st.subheader("🗺️ Mapa Interativo da RMC")
        
        # Criar mapa com Folium
        m = folium.Map(
            location=[-22.9, -47.06], 
            zoom_start=10,
            tiles="cartodbpositron"
        )
        
        # Adicionar GeoJSON ao mapa
        folium.GeoJson(
            geojson_str,
            name="RMC",
            style_function=lambda feature: {
                'fillColor': '#4d648d',
                'color': '#1a2d5a',
                'weight': 1,
                'fillOpacity': 0.7
            },
            highlight_function=lambda x: {
                'weight': 3,
                'fillOpacity': 0.9
            },
            tooltip=folium.GeoJsonTooltip(
                fields=["name", "pib_2021", "populacao_2022"],
                aliases=["Município", "PIB (2021)", "População (2022)"],
                localize=True
            )
        ).add_to(m)
        
        # Destacar município selecionado
        for feature in geojson['features']:
            if feature['properties']['name'] == selected_municipio:
                folium.GeoJson(
                    feature,
                    name="Selecionado",
                    style_function=lambda x: {
                        'fillColor': '#d62728',
                        'color': '#d62728',
                        'weight': 2,
                        'fillOpacity': 0.9
                    }
                ).add_to(m)
                break
        
        folium_static(m, width=900, height=600)

with tab2:
    st.subheader(f"📊 Comparativo entre Municípios - {selected_municipio}")
    
    if show_graphs:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras - PIB
            fig = px.bar(
                df.sort_values('pib_2021', ascending=False),
                x='pib_2021',
                y=df.index,
                orientation='h',
                title='PIB dos Municípios (2021)',
                labels={'pib_2021': 'PIB (R$)', 'index': 'Município'},
                color_discrete_sequence=['#4d648d']
            )
            fig.update_layout(height=500)
            # Destacar município selecionado
            fig.update_traces(marker_color=['#d62728' if x == selected_municipio else '#4d648d' for x in df.index])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de pizza - Participação no PIB regional
            fig = px.pie(
                df,
                values='participacao_rmc',
                names=df.index,
                title='Participação no PIB Regional',
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            # Destacar município selecionado
            fig.update_traces(
                pull=[0.1 if x == selected_municipio else 0 for x in df.index],
                marker_colors=['#d62728' if x == selected_municipio else '#4d648d' for x in df.index],
                textposition='inside'
            )
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("""
    Desenvolvido com Python, Streamlit e geoprocessamento. 
    Dados atualizados em 2023.
""")
