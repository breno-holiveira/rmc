import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Barra de navegação
st.markdown("""
<style>
#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

.block-container {
    padding-top: 60px !important;
    font-family: 'Georgia', serif;
}

.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 60px;
    background: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
    display: flex;
    align-items: center;
    padding: 0 40px;
    gap: 40px;
    font-family: 'Georgia', serif;
    z-index: 9999;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo-container {
    font-weight: 700;
    font-size: 28px;
    color: #343a40;
    user-select: none;
    cursor: default;
    display: flex;
    align-items: center;
}
.logo-container .data {
    font-weight: 400;
    font-size: 20px;
    color: #6c757d;
    margin-left: 5px;
}

.nav-item {
    position: relative;
    cursor: pointer;
}

.nav-link {
    color: #495057;
    font-size: 18px;
    padding: 15px 12px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    transition: color 0.3s ease, background 0.3s ease;
    border-radius: 4px;
}
.nav-link:hover {
    color: #ffffff;
    background: #007bff;
}

/* Triângulo para baixo normal */
.dropdown-arrow {
    margin-left: 5px;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #495057;
    transition: border-top-color 0.3s ease;
    display: inline-block;
    vertical-align: middle;
}
.nav-link:hover .dropdown-arrow {
    border-top-color: #ffffff;
}

.dropdown-content {
    position: absolute;
    top: 60px;
    left: 0;
    background: #ffffff;
    min-width: 180px;
    border-top: 2px solid #007bff;
    padding: 8px 0;
    display: none;
    font-family: 'Georgia', serif;
    border-radius: 0 0 4px 4px;
    z-index: 99999;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-item:hover .dropdown-content {
    display: block;
}

.dropdown-content a {
    color: #495057;
    padding: 10px 16px;
    font-size: 16px;
    text-decoration: none;
    display: block;
    transition: color 0.3s ease, background 0.3s ease;
}
.dropdown-content a:hover {
    color: #ffffff;
    background: #007bff;
    font-weight: normal;
}
</style>

<div class="navbar">
    <div class="logo-container">RMC<span class="data">Data</span></div>
    <div class="nav-item">
        <a href="#" class="nav-link" target="_self">Início</a>
    </div>
    <div class="nav-item">
        <span class="nav-link">Economia <span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="#" target="_self">PIB</a>
            <a href="#" target="_self">PIB per capita</a>
            <a href="#" target="_self">VAB</a>
        </div>
    </div>
    <div class="nav-item">
        <span class="nav-link">Finanças <span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="#" target="_self">Orçamento</a>
            <a href="#" target="_self">Tributos</a>
        </div>
    </div>
    <div class="nav-item">
        <span class="nav-link">Segurança <span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="#" target="_self">Câmeras</a>
            <a href="#" target="_self">Alertas</a>
        </div>
    </div>
    <div class="nav-item">
        <a href="#" class="nav-link" target="_self">Contato</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Conteúdo de exemplo
st.write("Bem-vindo ao RMC Data! Selecione uma opção na barra de navegação acima para explorar os dados.")
