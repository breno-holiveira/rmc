import streamlit as st
import geopandas as gpd
import json
import streamlit.components.v1 as components

st.title('RMC Data')

st.set_page_config(layout="wide")

st.header('Dados e indicadores da Região Metropolitana de Campinas')

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

# Carrega shapefile e ajusta CRS
gdf = gpd.read_file("./shapefile_rmc/RMC_municipios.shp")
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
gdf = gdf.sort_values(by="NM_MUN")

# Monta GeoJSON com propriedades extras
geojson = {"type": "FeatureCollection", "features": []}
for _, row in gdf.iterrows():
    name = row["NM_MUN"]
    geom = row["geometry"].__geo_interface__
    extra = dados_extra.get(name, {"populacao": None, "area": None, "pib_2021": None})
    geojson["features"].append({
        "type": "Feature",
        "properties": {
            "name": name,
            "populacao": extra["populacao"],
            "area": extra["area"],
            "pib_2021": extra["pib_2021"],
        },
        "geometry": geom
    })

geojson_str = json.dumps(geojson)

import streamlit as st

# Lê o conteúdo do HTML
with open("grafico.html", "r", encoding="utf-8") as f:
    html_code = f.read()

# Mostra o HTML no Streamlit
st.components.v1.html(html_code, height=950, scrolling=True)

