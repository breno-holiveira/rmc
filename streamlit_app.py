import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(initial_sidebar_state="collapsed")

# Injetando CSS para corrigir hover e remover negrito da aba ativa
st.markdown("""
<style>
    .stHorizontalBlock span {
        font-weight: 400 !important;           /* Remove negrito */
        padding: 7px 10px !important;          /* Padding proporcional */
        margin: 0 4px !important;
        border-radius: 8px !important;
        transition: background-color 0.25s ease;
    }
    .stHorizontalBlock [aria-selected="true"] span {
        background-color: rgba(255, 255, 255, 0.25) !important;
        font-weight: 400 !important;
    }
    .stHorizontalBlock span:hover {
        background-color: rgba(255, 255, 255, 0.35) !important;
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
