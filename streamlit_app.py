import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="collapsed")

# HTML do menu de navegação
html_navbar = """
<style>
/* Container principal */
.navbar {
    display: flex;
    align-items: center;
    background-color: #0B1D3A;
    padding: 0.5rem 1rem;
    font-family: 'Segoe UI', sans-serif;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Logo */
.navbar img {
    height: 32px;
    margin-right: 16px;
}

/* Links */
.navbar a {
    color: #E0E6F0;
    text-decoration: none;
    padding: 10px 16px;
    border-radius: 6px;
    margin-right: 6px;
    transition: background-color 0.3s ease;
    font-size: 15px;
}

/* Hover */
.navbar a:hover {
    background-color: #1F355A;
    color: #FFFFFF;
}

/* Ativo */
.navbar a.active {
    background-color: #1F355A;
    font-weight: bold;
}
</style>

<div class="navbar">
    <img src="https://raw.githubusercontent.com/breno-holiveira/rmc/main/cubes.svg" alt="Logo">
    <a href="/?page=inicio" class="active">Início</a>
    <a href="/?page=sobre">Sobre</a>
    <a href="/?page=economia">Economia</a>
    <a href="/?page=financas">Finanças</a>
    <a href="/?page=seguranca">Segurança</a>
    <a href="https://github.com/breno-holiveira/rmc" target="_blank">GitHub</a>
</div>
"""

# Exibir a navbar HTML
components.html(html_navbar, height=60)

# Lógica de navegação por parâmetro de URL
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["inicio"])[0]

# Lógica de renderização baseada no "page"
if page == "inicio":
    st.title("Página Início")
elif page == "sobre":
    st.title("Página Sobre")
elif page == "economia":
    st.title("Página Economia")
elif page == "financas":
    st.title("Página Finanças")
elif page == "seguranca":
    st.title("Página Segurança")
else:
    st.title("Página não encontrada")
