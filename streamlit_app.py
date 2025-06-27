import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(
    page_title="Exemplo com Navbar Verde",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Lista de páginas
pages = ["Home", "Library", "Tutorials", "Development", "Download"]

# Estilo verde claro
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

# Mostra a navbar e guarda a aba atual
page = st_navbar(pages, styles=styles)

# Conteúdo por página
if page == "Home":
    st.title("Home")
    st.write("Bem-vindo à página inicial.")

elif page == "Library":
    st.title("Library")
    st.write("Catálogo e repositórios de dados.")

elif page == "Tutorials":
    st.title("Tutorials")
    st.write("Guias de uso e demonstrações práticas.")

elif page == "Development":
    st.title("Development")
    st.write("Notas sobre desenvolvimento e roadmap.")

elif page == "Download":
    st.title("Download")
    st.write("Arquivos disponíveis para baixar.")

# Sidebar opcional
with st.sidebar:
    st.write("Sidebar")
