import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(initial_sidebar_state="collapsed")

# Força a fonte correta (igual à do site OUP)
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, sans-serif !important;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

pages = ["Home", "Library", "Tutorials", "Development", "Download"]

styles = {
    "nav": {
        "background-color": "rgb(123, 209, 146)",  # Ou "#1f2937" se quiser azul escuro
        "font-family": "system-ui, sans-serif",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(49, 51, 63)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
        "font-size": "16px",
        "font-weight": "500",
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
