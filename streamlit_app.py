import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(page_title="RMC Data", layout="wide")

# Injetar CSS ultrafino para navbar
st.markdown("""
<style>
[data-testid="stHorizontalBlock"] > div:first-child {
    background-color: #1f2937 !important;
    padding: 0 !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
}

[data-testid="stHorizontalBlock"] button, 
[data-testid="stHorizontalBlock"] div[role="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: rgba(255,255,255,0.85) !important;
    padding: 4px 8px !important;
    margin: 0 6px !important;
    border-radius: 0 !important;
    background-color: transparent !important;
    border: none !important;
    cursor: pointer;
    transition: color 0.2s ease !important;
    white-space: nowrap;
}

[data-testid="stHorizontalBlock"] button:hover,
[data-testid="stHorizontalBlock"] div[role="tab"]:hover {
    color: #ffa366 !important;
}

[data-testid="stHorizontalBlock"] button[aria-selected="true"],
[data-testid="stHorizontalBlock"] div[role="tab"][aria-selected="true"] {
    color: #fff !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    border-bottom: 2px solid rgba(255, 163, 102, 0.9) !important;
    padding-bottom: 4px !important;
    margin-bottom: 0 !important;
}

[data-testid="stHorizontalBlock"] button:focus,
[data-testid="stHorizontalBlock"] div[role="tab"]:focus {
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "4px 8px",
        "font-weight": "400",
        "margin": "0 6px",
    },
    "active": {
        "color": "#fff",
        "font-weight": "500",
        "border-bottom": "2px solid rgba(255, 163, 102, 0.9)",
        "padding-bottom": "4px",
    }
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

pages = ["Inicio", "Documentation", "Examples", "Community", "About"]
page = st_navbar(pages, styles=styles, options=options)

st.write(f"Você está na página: {page}")
