import streamlit as st

st.set_page_config(page_title='RMC Data', layout='wide', initial_sidebar_state='collapsed')

# Inicializa a página padrão
if "page" not in st.session_state:
    st.session_state.page = "inicio"

# Função para mudar de página
def switch_page(page):
    st.session_state.page = page

# Estilo e HTML da navbar com JS para atualizar session_state
navbar_html = """
<style>
    .navbar {
        background-color: #0B1D3A;
        padding: 0 2rem;
        height: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: Arial, sans-serif;
    }
    .navbar-title {
        color: white;
        font-size: 22px;
        font-weight: bold;
        margin-right: 30px;
    }
    .nav-links {
        display: flex;
        gap: 0;
        height: 100%;
    }
    .nav-item {
        position: relative;
        height: 100%;
    }
    .nav-button {
        color: #E0E6F0;
        background: none;
        border: none;
        padding: 0 20px;
        height: 100%;
        display: flex;
        align-items: center;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.1s ease;
    }
    .nav-button:hover {
        color: white;
        background-color: #1F355A;
    }
    .dropdown-content {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: #0B1D3A;
        min-width: 180px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
        display: none;
        border-top: 2px solid #2D4375;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    .dropdown-item {
        color: #E0E6F0;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.1s ease;
        border-left: 3px solid transparent;
    }
    .dropdown-item:hover {
        background-color: #1F355A;
        border-left: 3px solid #4F46E5;
    }
</style>

<div class="navbar">
    <div class="navbar-title">RMC Data</div>
    <div class="nav-links">
        <div class="nav-item">
            <form action="" method="post">
                <button class="nav-button" name="nav" value="inicio">Início</button>
            </form>
        </div>
        <div class="nav-item">
            <form action="" method="post">
                <button class="nav-button" name="nav" value="sobre">Sobre</button>
            </form>
        </div>
        <div class="nav-item">
            <form action="" method="post">
                <button class="nav-button" name="nav" value="economia">Economia</button>
            </form>
        </div>
        <div class="nav-item dropdown">
            <button class="nav-button">Finanças</button>
            <div class="dropdown-content">
                <form action="" method="post">
                    <button class="dropdown-item" name="nav" value="financas">📊 Finanças</button>
                    <button class="dropdown-item" name="nav" value="despesas">💸 Despesas</button>
                    <button class="dropdown-item" name="nav" value="arrecadacao">💰 Arrecadação</button>
                </form>
            </div>
        </div>
    </div>
</div>
"""

# Lê os botões HTML como POST
nav = st.experimental_get_query_params().get("nav", [None])[0]
if st.session_state.get("nav_button_pressed"):
    nav = st.session_state["nav_button_pressed"]

# Detecta clique nos botões
if "nav" in st.experimental_get_query_params():
    switch_page(nav)
elif st._is_running_with_streamlit:
    if "nav" in st.requested_url_query_params:
        switch_page(st.requested_url_query_params["nav"])

# Manipular POST manualmente (hack simples)
form_data = st.experimental_get_query_params()
if "nav" in form_data:
    st.session_state.page = form_data["nav"][0]

# Renderizar HTML
st.markdown(navbar_html, unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# Mostrar a página correspondente
page = st.session_state.page

if page == "inicio":
    st.title("Início")
    st.write("Bem-vindo ao Sistema RMC Data.")
elif page == "sobre":
    st.title("Sobre")
    st.write("Página sobre o projeto.")
elif page == "economia":
    st.title("Economia")
    st.write("Indicadores e estatísticas econômicas da RMC.")
elif page == "financas":
    st.title("Finanças")
    st.write("Análise financeira da região.")
elif page == "despesas":
    st.title("Finanças > Despesas")
    st.write("Dados sobre despesas públicas.")
elif page == "arrecadacao":
    st.title("Finanças > Arrecadação")
    st.write("Receitas e arrecadação pública.")
else:
    st.error("Página não encontrada.")
