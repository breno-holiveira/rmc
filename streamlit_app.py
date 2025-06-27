import streamlit as st

nav_html = """
<style>
.navbar {
    background-color: #0B1D3A;
    padding: 1rem;
    display: flex;
    gap: 1.5rem;
    font-family: Arial, sans-serif;
}
.nav-link {
    color: #E0E6F0;
    text-decoration: none;
    font-size: 15px;
    padding: 8px 12px;
}
.nav-link:hover {
    background-color: #1F355A;
    border-radius: 4px;
    color: white;
}
</style>

<div class="navbar">
    <a class="nav-link" href="/">Início</a>
    <a class="nav-link" href="/sobre">Sobre</a>
    <a class="nav-link" href="/economia">Economia</a>
    <a class="nav-link" href="/financas">Finanças</a>
    <a class="nav-link" href="/despesas">Despesas</a>
    <a class="nav-link" href="/arrecadacao">Arrecadação</a>
</div>
"""

st.markdown(nav_html, unsafe_allow_html=True)
