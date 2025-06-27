import streamlit as st
from streamlit_navigation_bar import st_navbar

# Configuração da página
st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊")

# Estilo básico para a navbar
styles = {
    "nav": {
        "background-color": "royalblue",
        "justify-content": "left",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Definir páginas
pages = ["Home", "Documentation", "Examples", "Community", "About"]
page = st_navbar(pages, styles=styles, options=options)

# Só mostrar qual aba está selecionada (sem conteúdo)
st.write(f"Página selecionada: **{page}**")
