import os
import streamlit as st
from streamlit_navigation_bar import st_navbar

st.set_page_config(initial_sidebar_state="collapsed")

pages = ["Install", "User Guide", "API", "Examples", "Community", "GitHub"]
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, "cubes.svg")
urls = {"GitHub": "https://github.com/gabrieltempass/streamlit-navigation-bar"}

styles = {
    "nav": {
        "background-color": "royalblue",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "white",
        "padding": "14px",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "normal",
        "padding": "14px",
    }
}
options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    logo_path=logo_path,
    urls=urls,
    styles=styles,
    options=options,
)

# Definindo funções internas para cada página

def show_install():
    st.title("Install")
    st.write("Conteúdo da página de instalação.")

def show_user_guide():
    st.title("User Guide")
    st.write("Conteúdo do guia do usuário.")

def show_api():
    st.title("API")
    st.write("Documentação da API.")

def show_examples():
    st.title("Examples")
    st.write("Exemplos de uso.")

def show_community():
    st.title("Community")
    st.write("Informações da comunidade.")

def show_github():
    st.title("GitHub")
    st.write("Link para o repositório:")
    st.markdown("[streamlit-navigation-bar](https://github.com/gabrieltempass/streamlit-navigation-bar)")

# Mapeamento de página para função
functions = {
    "Install": show_install,
    "User Guide": show_user_guide,
    "API": show_api,
    "Examples": show_examples,
    "Community": show_community,
    "GitHub": show_github,
}

# Executa a função da página selecionada
go_to = functions.get(page)
if go_to:
    go_to()
