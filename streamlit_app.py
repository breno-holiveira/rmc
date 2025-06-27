import os
import streamlit as st
from streamlit_navigation_bar import st_navbar

import pages as pg

st.set_page_config(page_title="RMC Data", layout="wide", page_icon="📊", initial_sidebar_state="collapsed")

pages = ["Home", "Install", "User Guide", "API", "Examples", "Community", "GitHub"]

urls = {"GitHub": "https://github.com/gabrieltempass/streamlit-navigation-bar"}

styles = {
    "nav": {
        "background-color": "#1e293b",  # azul escuro sóbrio
        "justify-content": "left",
        "position": "relative",  # Para o texto absoluto funcionar
        "padding": "0 2rem",
        "height": "60px",
        "font-family": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "font-size": "1rem",
    },
    "span": {
        "color": "white",
        "padding": "14px",
        "font-weight": "600",
    },
    "active": {
        "background-color": "#334155",  # fundo ativo suave
        "color": "#facc15",  # amarelo queimado
        "font-weight": "700",
        "padding": "14px",
    },
    "img": {  # mantido só para manter compatibilidade
        "display": "none",  # escondendo o ícone
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    logo_path=None,  # retirando ícone para usar texto
    urls=urls,
    styles=styles,
    options=options,
)

# CSS para o logo-text clicável "RMC DATA"
logo_text_css = """
<style>
.logo-text {
    position: absolute;
    top: 50%;
    left: 2rem;
    transform: translateY(-50%);
    font-size: 1.4rem;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    color: #ddd;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.3s ease;
    text-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
    user-select: none;
    z-index: 10000;
}
.logo-text:hover {
    color: #d97722; /* laranja queimado suave */
}
</style>
"""

st.markdown(logo_text_css, unsafe_allow_html=True)

# Logo-text clicável com link para página Home
st.markdown(
    """
    <a href='/?page=Home' class='logo-text'>RMC DATA</a>
    """,
    unsafe_allow_html=True
)

functions = {
    "Home": pg.show_home,
    "Install": pg.show_install,
    "User Guide": pg.show_user_guide,
    "API": pg.show_api,
    "Examples": pg.show_examples,
    "Community": pg.show_community,
}

go_to = functions.get(page)
if go_to:
    go_to()
else:
    st.write("Selecione uma página no menu.")
