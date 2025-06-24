import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import json

# Configurações da página Streamlit
st.set_page_config(
    page_title="RMC Data - Região Metropolitana de Campinas",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de cores suave, minimalista e profissional
PRIMARY_COLOR = "#0b3d91"  # Azul elegante
BACKGROUND_COLOR = "#f9fafb"  # Branco gelo/off-white
TEXT_COLOR = "#222222"

# Dados extras - população, área e PIB (exemplo)
dados_extra = {
    "Americana": {"populacao": 240000, "area": 140.5, "pib_2021": 12_500_000_000},
    "Artur Nogueira": {"populacao": 56000, "area": 140.2, "pib_2021": 2_200_000_000},
    "Campinas": {"populacao": 1200000, "area": 796.0, "pib_2021": 105_000_000_000},
    "Cosmópolis": {"populacao": 70000, "area": 154.5, "pib_2021": 3_100_000_000},
    "Engenheiro Coelho": {"populacao": 17000, "area": 130.1, "pib_2021": 900_000_000},
    "Holambra": {"populacao": 13000, "area": 65.7, "pib_2021": 850_000_000},
    "Hortolândia": {"populacao": 240000, "area": 62.5, "pib_2021": 9_500_000_000},
    "Indaiatuba": {"populacao": 260000, "area": 311.4, "pib_2021": 15_000_000_000},
    "Itatiba": {"populacao": 120000, "area": 322.3, "pib_2021": 6_500_000_000},
    "Jaguariúna": {"populacao": 57000, "area": 141.2, "pib_2021": 3_200_000_000},
    "Monte Mor": {"populacao": 46000, "area": 155.1, "pib_2021": 2_700_000_000},
    "Morungaba": {"populacao": 14000, "area": 146.4, "pib_2021": 1_100_000_000},
    "Nova Odessa": {"populacao": 62000, "area": 73.3, "pib_2021": 3_600_000_000},
    "Paulínia": {"populacao": 110000, "area": 131.3, "pib_2021": 18_500_000_000},
    "Santa Bárbara d'Oeste": {"populacao": 210000, "area": 310.4, "pib_2021": 10_500_000_000},
    "Santo Antônio de Posse": {"populacao": 31000, "area": 154.0, "pib_2021": 1_600_000_000},
    "Sumaré": {"populacao": 280000, "area": 153.3, "pib_2021": 14_200_000_000},
    "Valinhos": {"populacao": 125000, "area": 148.0, "pib_2021": 7_400_000_000},
    "Vinhedo": {"populacao": 80000, "area": 148.8, "pib_2021": 5_900_000_000},
}

@st.cache_data(show_spinner=True)
def load_shapefile(path="./shapefile_rmc/RMC_municipios.shp"):
    gdf = gpd.read_file(path)
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    gdf = gdf.sort_values("NM_MUN").reset_index(drop=True)
    return gdf

@st.cache_data
def prepare_dataframe(gdf, extra_data):
    df = gdf[["NM_MUN", "geometry"]].copy()
    df["populacao"] = df["NM_MUN"].map(lambda x: extra_data.get(x, {}).get("populacao"))
    df["area"] = df["NM_MUN"].map(lambda x: extra_data.get(x, {}).get("area"))
    df["pib_2021"] = df["NM_MUN"].map(lambda x: extra_data.get(x, {}).get("pib_2021"))
    return df

# Carregar dados
gdf = load_shapefile()
df = prepare_dataframe(gdf, dados_extra)

# --- Sidebar ---
st.sidebar.header("Filtros e Seleção")

municipios = df["NM_MUN"].tolist()
selected_municipio = st.sidebar.selectbox("Selecione o município", ["Todos"] + municipios)

# Filtrar dados para gráfico e mapa
if selected_municipio != "Todos":
    df_filtrado = df[df["NM_MUN"] == selected_municipio]
else:
    df_filtrado = df.copy()

# --- Mapa interativo com Folium ---
st.subheader("Mapa Interativo - Municípios da RMC")

# Criar mapa centrado em Campinas
map_center = [-22.9, -47.06]  # latitude, longitude aproximada Campinas
m = folium.Map(location=map_center, zoom_start=10, tiles="CartoDB Positron")

# Adicionar polígonos dos municípios ao mapa
for idx, row in df_filtrado.iterrows():
    name = row["NM_MUN"]
    pop = row["populacao"]
    area = row["area"]
    pib = row["pib_2021"]

    geo_json = folium.GeoJson(
        row["geometry"],
        name=name,
        style_function=lambda feature: {
            "fillColor": PRIMARY_COLOR,
            "color": PRIMARY_COLOR,
            "weight": 2,
            "fillOpacity": 0.2,
        },
        highlight_function=lambda feature: {
            "weight": 3,
            "color": "#1d2a6f",
            "fillOpacity": 0.35,
        },
        tooltip=folium.Tooltip(f"<b>{name}</b><br>População: {pop:,}<br>Área: {area:.1f} km²<br>PIB 2021: R$ {pib:,}"),
    )
    geo_json.add_to(m)

# Renderizar mapa no Streamlit
st_data = st_folium(m, width=900, height=600)

# --- Gráfico interativo Plotly ---
st.subheader("Indicadores dos Municípios")

# Formatar dados para gráfico
df_plot = df_filtrado.copy()
df_plot["pib_milhoes"] = df_plot["pib_2021"] / 1_000_000  # PIB em milhões para visualização

# Gráfico de barras com Plotly Express
fig = px.bar(
    df_plot,
    x="NM_MUN",
    y=["populacao", "area", "pib_milhoes"],
    barmode="group",
    labels={
        "NM_MUN": "Município",
        "value": "Valor",
        "variable": "Indicador",
        "populacao": "População",
        "area": "Área (km²)",
        "pib_milhoes": "PIB 2021 (milhões R$)",
    },
    title="Comparação dos Indicadores dos Municípios",
    color_discrete_map={
        "populacao": "#0b3d91",
        "area": "#4682B4",
        "pib_milhoes": "#a0b8f0"
    },
)

fig.update_layout(
    legend_title_text="Indicadores",
    plot_bgcolor=BACKGROUND_COLOR,
    paper_bgcolor=BACKGROUND_COLOR,
    font=dict(color=TEXT_COLOR),
    margin=dict(l=20, r=20, t=50, b=20),
    xaxis_tickangle=-45,
)

# Exibe gráfico
st.plotly_chart(fig, use_container_width=True)

# --- Painel resumo/detalhes ---
st.subheader("Resumo Detalhado")

if selected_municipio == "Todos":
    st.info("Selecione um município para ver detalhes específicos.")
else:
    data_sel = df_filtrado.iloc[0]
    st.markdown(f"""
    <div style="background-color: #f0f4ff; padding: 20px; border-radius: 8px; color: {TEXT_COLOR};">
        <h3 style="color: {PRIMARY_COLOR}; margin-top: 0;">{data_sel.NM_MUN}</h3>
        <ul style="list-style-type:none; padding-left: 0;">
            <li><strong>População:</strong> {data_sel.populacao:,}</li>
            <li><strong>Área:</strong> {data_sel.area:.1f} km²</li>
            <li><strong>PIB (2021):</strong> R$ {data_sel.pib_2021:,}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- Rodapé estilizado ---
st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
