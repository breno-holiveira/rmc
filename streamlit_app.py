import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(initial_sidebar_state="collapsed")

# Aplica uma fonte suave e estiliza apenas a parte visual
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }
    .stHorizontalBlock {
        padding: 0.25rem 0.75rem !important;
        background-color: rgb(123, 209, 146) !important;
        border-radius: 0.5rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stHorizontalBlock span {
        font-size: 15px !important;
        font-weight: 400 !important;
        padding: 0.4375rem 0.625rem !important;
        margin: 0 0.125rem !important;
        border-radius: 0.5rem !important;
        color: rgb(49, 51, 63) !important;
        transition: background-color 0.25s ease;
    }
    .stHorizontalBlock [aria-selected="true"] span {
        background-color: rgba(255, 255, 255, 0.25) !important;
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
