import streamlit as st

# Configuração da página
st.set_page_config(
    page_title='RMC Data',
    initial_sidebar_state='collapsed',
    layout='wide'
)

# CSS e HTML personalizado com melhorias
nav_html = """
<style>
    /* Fontes importadas */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    /* Reset e estilos base */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Barra de navegação principal */
    .navbar {
        background-color: #0B1D3A;
        padding: 0 2rem;
        height: 70px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1000;
    }
    
    /* Logo/Texto RMC Data */
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .brand-logo {
        height: 42px;
        width: 42px;
        background: linear-gradient(135deg, #4F46E5, #06B6D4);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 18px;
    }
    
    .brand-text {
        color: white;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 0.5px;
        background: linear-gradient(to right, #E0E6F0, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Itens do menu */
    .nav-links {
        display: flex;
        gap: 5px;
        height: 100%;
    }
    
    .nav-item {
        position: relative;
        height: 100%;
        display: flex;
        align-items: center;
    }
    
    .nav-link {
        color: #E0E6F0;
        text-decoration: none;
        padding: 0 22px;
        height: 100%;
        display: flex;
        align-items: center;
        font-size: 15px;
        font-weight: 500;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .nav-link:hover {
        color: white;
        background-color: rgba(255,255,255,0.05);
    }
    
    .nav-link.active {
        color: white;
        font-weight: 600;
    }
    
    /* Efeito hover */
    .nav-link::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 3px;
        background: linear-gradient(to right, #4F46E5, #06B6D4);
        transition: width 0.3s ease;
    }
    
    .nav-link:hover::after {
        width: 60%;
    }
    
    /* Dropdown menu */
    .dropdown {
        position: relative;
    }
    
    .dropdown-content {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: white;
        min-width: 220px;
        border-radius: 8px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        opacity: 0;
        visibility: hidden;
        transform: translateY(10px);
        transition: all 0.3s ease;
        z-index: 100;
        padding: 8px 0;
    }
    
    .dropdown:hover .dropdown-content {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
    }
    
    .dropdown-item {
        padding: 12px 20px;
        color: #4B5563;
        text-decoration: none;
        display: block;
        transition: all 0.2s ease;
        font-size: 14px;
    }
    
    .dropdown-item:hover {
        background-color: #F3F4F6;
        color: #1F2937;
        padding-left: 25px;
    }
    
    /* Ícone de seta */
    .dropdown-icon {
        margin-left: 6px;
        transition: transform 0.3s ease;
    }
    
    .dropdown:hover .dropdown-icon {
        transform: rotate(180deg);
    }
    
    /* Responsividade para telas menores */
    @media (max-width: 992px) {
        .navbar {
            padding: 0 1rem;
        }
        
        .nav-link {
            padding: 0 15px;
            font-size: 14px;
        }
    }
</style>

<!-- Estrutura da navbar -->
<div class="navbar">
    <!-- Logo/Marca -->
    <div class="brand">
        <div class="brand-logo">RMC</div>
        <div class="brand-text">Data Analytics</div>
    </div>
    
    <!-- Links de navegação -->
    <div class="nav-links">
        <div class="nav-item">
            <a href="#" class="nav-link active">Home</a>
        </div>
        
        <div class="nav-item dropdown">
            <a href="#" class="nav-link">
                About
                <svg class="dropdown-icon" width="12" height="8" viewBox="0 0 12 8" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 1L6 6L11 1" stroke="#E0E6F0" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </a>
            <div class="dropdown-content">
                <a href="#" class="dropdown-item">Our Team</a>
                <a href="#" class="dropdown-item">Mission/Vision</a>
                <a href="#" class="dropdown-item">History</a>
                <a href="#" class="dropdown-item">Partners</a>
            </div>
        </div>
        
        <div class="nav-item dropdown">
            <a href="#" class="nav-link">
                Solutions
                <svg class="dropdown-icon" width="12" height="8" viewBox="0 0 12 8" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 1L6 6L11 1" stroke="#E0E6F0" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </a>
            <div class="dropdown-content">
                <a href="#" class="dropdown-item">Economy Analysis</a>
                <a href="#" class="dropdown-item">Financial Tools</a>
                <a href="#" class="dropdown-item">Security Metrics</a>
                <a href="#" class="dropdown-item">Custom Solutions</a>
            </div>
        </div>
        
        <div class="nav-item">
            <a href="#" class="nav-link">Clients</a>
        </div>
        
        <div class="nav-item">
            <a href="https://github.com/breno-holiveira/rmc" target="_blank" class="nav-link">GitHub</a>
        </div>
    </div>
</div>
"""

# Renderização da navbar
st.markdown(nav_html, unsafe_allow_html=True)

# Conteúdo principal da página
st.title("Bem-vindo ao Portal RMC Data")
st.write("""
Explore nossos dashboards e ferramentas de análise de dados. Utilize o menu acima para navegar entre as seções.
""")
