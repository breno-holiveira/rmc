import streamlit as st
import pandas as pd
import geopandas as gpd
import json
from streamlit_navigation_bar import st_navbar

# Importar fonte Inter para legibilidade
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <style>
        .stHorizontalBlock span {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-weight: 400 !important;
            font-size: 15px !important;
            letter-spacing: 0em !important;
            padding: 6px 6px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.8) !important;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: relative;
            transition: color 0.25s ease;
        }
        .stHorizontalBlock span:hover {
            color: #ffa366 !important;
        }
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 500 !important;
            color: #ff8c42 !important;
        }
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: 0;
            height: 2px;
            width: 100%;
            background-color: #ff8c42;
            border-radius: 2px;
            transition: width 0.3s ease;
            animation: underlineExpand 0.3s forwards;
        }
        .stHorizontalBlock {
            background-color: #1f2937 !important;
            padding: 0 !important;
            height: 42px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
        }
        @keyframes underlineExpand {
            from { width: 0; }
            to { width: 100%; }
        }
        /* Visual indent para sub-itens */
        .sub-item {
            font-size: 13px !important;
            padding-left: 18px !important;
            color: rgba(255,255,255,0.65) !important;
        }
        .sub-item[aria-selected="true"] span {
            font-weight: 500 !important;
            color: #ffb374 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
    },
    "span": {
        "color": "rgba(255,255,255,0.8)",
        "padding": "6px 6px",
        "font-weight": "400",
        "font-size": "15px",
        "letter-spacing": "0em",
        "margin": "0 6px",
        "white-space": "nowrap",
        "position": "relative",
    },
    "active": {
        "color": "#ff8c42",
        "font-weight": "500",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Lista com itens principais e sub-itens (os sub-itens começam com tabulação para hierarquia visual)
pages = [
    "Inicio",
    "Documentation",
    "Examples",
    "  Example 1",
    "  Example 2",
    "  Example 3",
    "Community",
    "About"
]

page = st_navbar(pages, styles=styles, options=options)

# Lógica de seleção — ajustar para reconhecer sub-itens (com espaços no início)
def is_subitem(p):
    return p.startswith("  ")

if is_subitem(page):
    # Se for sub-item, remove os espaços para o título e decide conteúdo
    page_main = None
    page_sub = page.strip()
else:
    page_main = page
    page_sub = None

# Conteúdo conforme a seleção
if page_main == "Inicio":
    st.title("RMC Data 📊")
    st.markdown("## Dados e indicadores da Região Metropolitana de Campinas")
    # seu conteúdo da Home aqui...

elif page_main == "Documentation":
    st.title("Documentation")
    st.write("Aqui você pode colocar a documentação do seu app...")

elif page_main == "Examples" or page_sub in ["Example 1", "Example 2", "Example 3"]:
    st.title("Examples")

    # Se for subitem, mostra conteúdo do subitem, senão default para Example 1
    if page_sub == "Example 1":
        st.write("Conteúdo do Example 1")
    elif page_sub == "Example 2":
        st.write("Conteúdo do Example 2")
    elif page_sub == "Example 3":
        st.write("Conteúdo do Example 3")
    else:
        st.write("Conteúdo padrão para Examples")

elif page_main == "Community":
    st.title("Community")
    st.write("Links para a comunidade...")

elif page_main == "About":
    st.title("About")
    st.write("Sobre o projeto...")
