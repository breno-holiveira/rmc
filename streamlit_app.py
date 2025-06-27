import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(
    page_title="Navbar Teste",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Fonte global
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Estilos visuais refinados
pages = ["Home", "Library", "Tutorials", "Development", "Download"]
styles = {
    "nav": {
        "background-color": "rgb(123, 209, 146)",
        "padding": "0.4rem 1rem",
        "border-radius": "8px",
        "margin": "0 auto",
        "font-family": "'DM Sans', sans-serif",
        "font-size": "15px",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(49, 51, 63)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
        "transition": "background-color 0.25s ease",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

# Renderiza a navbar
page = st_navbar(pages, styles=styles)

# Exibe a aba selecionada
st.write(f"Página atual: **{page}**")

# Sidebar de teste
with st.sidebar:
    st.write("Sidebar de exemplo")
