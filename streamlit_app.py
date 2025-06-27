import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(initial_sidebar_state="collapsed")

# CSS para corrigir negrito e hover do st_navbar
st.markdown("""
<style>
/* Remove negrito e ajusta padding/margin para os botões da navbar */
.stHorizontalBlock span {
    font-weight: 400 !important;
    padding: 6px 12px !important;
    margin: 0 6px !important;
    border-radius: 6px !important;
    font-size: 15px !important;
    line-height: 1.4;
    transition: background-color 0.25s ease;
}

/* Aba ativa: sem negrito e com fundo suave */
.stHorizontalBlock [aria-selected="true"] span {
    background-color: rgba(255, 255, 255, 0.25) !important;
    font-weight: 400 !important;
    box-shadow: none !important;
}

/* Hover suave e proporcional */
.stHorizontalBlock span:hover {
    background-color: rgba(255, 255, 255, 0.35) !important;
    box-shadow: none !important;
}

/* Estilo da barra de navegação */
.stHorizontalBlock {
    padding: 4px 12px !important;
    border-radius: 8px !important;
    background-color: rgb(123, 209, 146) !important;
    margin-top: 8px !important;
    justify-content: center !important;
}
</style>
""", unsafe_allow_html=True)

pages = ["Home", "Library", "Tutorials", "Development", "Download"]

styles = {
    "nav": {
        "background-color": "rgb(123, 209, 146)",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(49, 51, 63)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

page = st_navbar(pages, styles=styles)
st.write(page)

with st.sidebar:
    st.write("Sidebar")
