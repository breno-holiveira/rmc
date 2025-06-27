import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(page_title='RMC Data',
                   initial_sidebar_state='collapsed',
                   page_icon='📈',
                   layout='wide')

pages = ['Início', 'Sobre', 'Economia', 'Finanças Públicas', 'Segurança']
styles = {
    "nav": {
        "background-color": "#0B1D3A",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "#E0E6F0",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "#2E4A7D",
        "color": "#FFFFFF",
    },
    "hover": {
        "background-color": "#1F355A",
        "color": "#FFFFFF",
    },
}

page = st_navbar(pages, styles=styles)
st.write(page)

with st.sidebar:
    st.write("Sidebar")
