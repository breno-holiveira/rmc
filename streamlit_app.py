import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(initial_sidebar_state="collapsed")

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
        "margin": "0 0.25rem",
        "padding": "0.5rem 0.75rem",
        "transition": "background-color 0.3s ease",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
        "font-weight": "bold",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

page = st_navbar(pages, styles=styles)
st.write(page)

with st.sidebar:
    st.write("Sidebar")
