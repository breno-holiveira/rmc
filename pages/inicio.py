import streamlit as st
import pandas as pd
import json
import os

def show():
    st.markdown("## Início")

    shapefile_path = os.path.join("shapefile_rmc", "RMC_municipios.shp")

    # --- TENTATIVA DE CARREGAR COM GEOPANDAS ---
    try:
        import geopandas as gpd
        gdf = gpd.read_file(shapefile_path)
        # Se quiser, faça algo com o gdf aqui:
        # st.write("Mapa carregado com geopandas:", gdf)
    except Exception as e:
        # “Silencia” o erro e mostra só um aviso leve
        st.warning("⚠️ Mapa indisponível no momento. Voltamos já!")
        # Opcional: log interno
        # st.write(f"Detalhe do erro (dev): {e}")

    # resto do seu conteúdo de Início…
    st.markdown("Bem‑vindo ao RMC Data! Aqui virá seu dashboard principal.")

    # … e por aí vai.
