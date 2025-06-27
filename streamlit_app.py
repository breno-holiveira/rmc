import streamlit as st
from streamlit_navigation_bar import st_navbar

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊",
)

# Estilo visual da navbar (sem negrito, fundo escuro, fonte DM Sans)
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
        .stHorizontalBlock span {
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 400 !important;
            font-size: 15px !important;
            padding: 6px 6px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.85) !important;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: relative;
            transition: color 0.25s ease;
        }
        .stHorizontalBlock span:hover {
            color: #ff9e3b !important;
        }
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 400 !important;
            color: #f4a259 !important;
        }
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: none !important;
        }
        .stHorizontalBlock {
            background-color: #1f2937 !important;
            padding: 0 !important;
            height: 44px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
            user-select: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Estilo para o componente da navbar
styles = {
    "nav": {
        "background-color": "#1f2937",
        "justify-content": "left",
        "font-family": "'DM Sans', sans-serif",
        "font-size": "15px",
    },
    "span": {
        "color": "rgba(255,255,255,0.85)",
        "padding": "6px 6px",
        "font-weight": "400",
        "font-size": "15px",
        "margin": "0 6px",
        "white-space": "nowrap",
        "position": "relative",
    },
    "active": {
        "color": "#f4a259",
        "font-weight": "400",
    },
}

options = {
    "show_menu": False,
    "show_sidebar": False,
}

# Definição das páginas
pages = [
    "RMC Data",
    "Economia",
    "Finanças Públicas",
    "Segurança",
    "Arquivos",
    "Sobre",
    "Contato",
]

# Controle de navegação
if "page" not in st.session_state:
    st.session_state.page = pages[0]

clicked_page = st_navbar(pages, logo_path=None, styles=styles, options=options)

if clicked_page and clicked_page != st.session_state.page:
    st.session_state.page = clicked_page

page = st.session_state.page

# Conteúdo de cada página (mock)
if page == "RMC Data":
    st.title("RMC Data 📊")
    st.markdown("### Página inicial com resumo da Região Metropolitana de Campinas.")

elif page == "Economia":
    st.title("Economia")
    st.write("Página com indicadores econômicos da região.")

elif page == "Finanças Públicas":
    st.title("Finanças Públicas")
    st.write("Página com informações fiscais e orçamentárias.")

elif page == "Segurança":
    st.title("Segurança")
    st.write("Dados sobre segurança pública e criminalidade.")

elif page == "Arquivos":
    st.title("Arquivos")
    st.write("Seção de download de documentos e relatórios.")

elif page == "Sobre":
    st.title("Sobre")
    st.write("Informações gerais sobre o projeto e objetivos.")

elif page == "Contato":
    st.title("Contato")
    st.write("Formas de contato e redes institucionais.")
