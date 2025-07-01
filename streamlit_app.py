import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Barra de navegação científica e institucional
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap');

#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

.block-container {
    padding-top: 64px !important;
    font-family: 'Merriweather', serif;
    background-color: #f9fafc;
    color: #2c2f36;
}

/* Barra superior */
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 64px;
    background: #ffffff;
    border-bottom: 1px solid #dee2e6;
    display: flex;
    align-items: center;
    padding: 0 48px;
    gap: 36px;
    font-family: 'Merriweather', serif;
    z-index: 10000;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* Logotipo */
.logo-container {
    font-weight: 700;
    font-size: 26px;
    color: #1c2e45;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
}
.logo-container .sub {
    font-weight: 400;
    font-size: 16px;
    color: #6c757d;
    margin-left: 6px;
}

/* Menu principal */
.nav-item {
    position: relative;
}

.nav-link {
    color: #344054;
    font-size: 17px;
    padding: 10px 14px;
    text-decoration: none;
    display: inline-block;
    border-radius: 4px;
    transition: background 0.3s ease, color 0.3s ease;
    cursor: pointer;
}
.nav-link:hover {
    background: #1c2e45;
    color: #ffffff;
}

/* Setinha de dropdown */
.dropdown-arrow {
    margin-left: 6px;
    width: 0; height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #344054;
    display: inline-block;
    vertical-align: middle;
    transition: border-top-color 0.3s ease;
}
.nav-link:hover .dropdown-arrow {
    border-top-color: #ffffff;
}

/* Dropdown */
.dropdown-content {
    position: absolute;
    top: 64px;
    left: 0;
    background: #ffffff;
    min-width: 180px;
    border: 1px solid #dee2e6;
    border-top: 3px solid #1c2e45;
    padding: 6px 0;
    display: none;
    font-family: 'Merriweather', serif;
    border-radius: 0 0 6px 6px;
    z-index: 10001;
    box-shadow: 0 6px 12px rgba(0,0,0,0.08);
}

.nav-item:hover .dropdown-content {
    display: block;
}

.dropdown-content a {
    color: #343a40;
    padding: 10px 20px;
    font-size: 15px;
    text-decoration: none;
    display: block;
    transition: background 0.2s ease, padding-left 0.2s;
}
.dropdown-content a:hover {
    background: #e9ecef;
    padding-left: 26px;
}
</style>

<!-- HTML da Barra de Navegação -->
<div class="navbar">
    <div class="logo-container">
        RMC<span class="sub">Data</span>
    </div>
    <div class="nav-item">
        <a href="#" class="nav-link" target="_self">Início</a>
    </div>
    <div class="nav-item">
        <span class="nav-link">Economia <span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="#" target="_self">PIB</a>
            <a href="#" target="_self">PIB per capita</a>
            <a href="#" target="_self">Valor Adicionado Bruto</a>
        </div>
    </div>
    <div class="nav-item">
        <span class="nav-link">Finanças <span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="#" target="_self">Orçamento</a>
            <a href="#" target="_self">Tributos</a>
            <a href="#" target="_self">Despesas</a>
        </div>
    </div>
    <div class="nav-item">
        <span class="nav-link">Segurança <span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="#" target="_self">Câmeras</a>
            <a href="#" target="_self">Alertas</a>
            <a href="#" target="_self">Comparativos</a>
        </div>
    </div>
    <div class="nav-item">
        <a href="#" class="nav-link" target="_self">Contato</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Conteúdo
st.write("Bem-vindo ao **RMC Data**! Utilize o menu superior para navegar pelos indicadores.")
