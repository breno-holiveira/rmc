import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para esconder elementos não necessários
st.markdown("""
<style>
#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}
.block-container {
    padding-top: 64px !important;
}
</style>
""", unsafe_allow_html=True)

# Barra de navegação premium internacional com HTML
st.markdown("""
<style>
.navbar-container {
    font-family: 'Georgia', serif;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    border-bottom: 1px solid #eaeaea;
    z-index: 1000;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 40px;
}

.logo {
    font-size: 22px;
    font-weight: 700;
    color: #333;
}
.logo .sub {
    font-weight: 400;
    font-size: 18px;
    color: #666;
}

.nav-links {
    display: flex;
    gap: 20px;
    height: 100%;
}

.nav-item {
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
}

.nav-link {
    color: #444;
    font-size: 15px;
    text-decoration: none;
    padding: 20px 12px;
    transition: color 0.2s;
    font-weight: 450;
    letter-spacing: 0.3px;
}

.nav-link:hover {
    color: #0056b3;
}

.dropdown-arrow {
    margin-left: 6px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid #666;
    transition: all 0.2s;
    display: inline-block;
}

.nav-item:hover .dropdown-arrow {
    border-top-color: #0056b3;
}

.dropdown-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background: white;
    min-width: 200px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    border: 1px solid #eaeaea;
    opacity: 0;
    visibility: hidden;
    transition: all 0.2s;
    z-index: 1001;
}

.nav-item:hover .dropdown-menu {
    opacity: 1;
    visibility: visible;
}

.dropdown-item {
    padding: 12px 16px;
    color: #444;
    font-size: 14px;
    text-decoration: none;
    display: block;
    transition: all 0.2s;
}

.dropdown-item:hover {
    background: #f8f9fa;
    color: #0056b3;
}

.divider {
    width: 1px;
    height: 24px;
    background: #eaeaea;
    margin: 0 10px;
}
</style>

<div class="navbar-container">
    <div class="logo">RMC<span class="sub">Data</span></div>
    
    <div class="nav-links">
        <div class="nav-item">
            <a href="#" class="nav-link">Home</a>
        </div>
        
        <div class="divider"></div>
        
        <div class="nav-item">
            <a href="#" class="nav-link">Economy <span class="dropdown-arrow"></span></a>
            <div class="dropdown-menu">
                <a href="#" class="dropdown-item">GDP</a>
                <a href="#" class="dropdown-item">GDP per capita</a>
                <a href="#" class="dropdown-item">VAB</a>
            </div>
        </div>
        
        <div class="nav-item">
            <a href="#" class="nav-link">Finance <span class="dropdown-arrow"></span></a>
            <div class="dropdown-menu">
                <a href="#" class="dropdown-item">Budget</a>
                <a href="#" class="dropdown-item">Taxes</a>
            </div>
        </div>
        
        <div class="nav-item">
            <a href="#" class="nav-link">Security <span class="dropdown-arrow"></span></a>
            <div class="dropdown-menu">
                <a href="#" class="dropdown-item">Cameras</a>
                <a href="#" class="dropdown-item">Alerts</a>
            </div>
        </div>
        
        <div class="divider"></div>
        
        <div class="nav-item">
            <a href="#" class="nav-link">Contact</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Conteúdo principal
st.markdown("<div style='margin-top: 80px;'></div>", unsafe_allow_html=True)
st.write("Welcome to RMC Data. Select an option from the navigation bar above.")
