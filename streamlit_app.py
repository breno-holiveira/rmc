import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Barra de navegação premium acadêmica
st.markdown("""
<style>
#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

.block-container {
    padding-top: 56px !important;
    font-family: 'Georgia', serif;
}

.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 56px;
    background: #ffffff;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    align-items: center;
    padding: 0 40px;
    gap: 30px;
    font-family: 'Georgia', serif;
    z-index: 9999;
}

.logo-container {
    font-weight: 700;
    font-size: 22px;
    color: #2a2a2a;
    user-select: none;
    cursor: default;
    display: flex;
    align-items: center;
    letter-spacing: 0.5px;
}
.logo-container .data {
    font-weight: 400;
    font-size: 18px;
    color: #5a5a5a;
    margin-left: 4px;
}

.nav-item {
    position: relative;
    cursor: pointer;
}

.nav-link {
    color: #4a4a4a;
    font-size: 16px;
    padding: 16px 12px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    transition: color 0.2s ease;
    font-weight: 450;
}

.nav-link:hover {
    color: #0077cc;
}

/* Triângulo para baixo */
.dropdown-arrow {
    margin-left: 5px;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid #5a5a5a;
    transition: border-top-color 0.2s ease;
    display: inline-block;
    vertical-align: middle;
}
.nav-link:hover .dropdown-arrow {
    border-top-color: #0077cc;
}

.dropdown-content {
    position: absolute;
    top: 56px;
    left: 0;
    background: #ffffff;
    min-width: 180px;
    padding: 8px 0;
    display: none;
    font-family: 'Georgia', serif;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border: 1px solid #e0e0e0;
    border-radius: 2px;
    z-index: 99999;
}

.nav-item:hover .dropdown-content {
    display: block;
}

.dropdown-content a {
    color: #4a4a4a;
    padding: 10px 16px;
    font-size: 15px;
    text-decoration: none;
    display: block;
    transition: background-color 0.2s ease;
}

.dropdown-content a:hover {
    background-color: #f7f7f7;
    color: #0077cc;
}

.nav-divider {
    height: 22px;
    border-left: 1px solid #e0e0e0;
    margin: 0 10px;
}

</style>

<div class="navbar">
    <div class="logo-container">RMC<span class="data">Data</span></div>
    
    <div class="nav-divider"></div>
    
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
    
    <div class="nav-divider"></div>
    
    <div class="nav-item">
        <a href="#" class="nav-link" target="_self">Contato</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Conteúdo de exemplo
st.write("Bem-vindo ao RMC Data! Selecione uma opção na barra de navegação acima para explorar os dados.")
