import streamlit as st

# Configuração da página com tema mais sóbrio
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# Barra de navegação acadêmica premium
st.markdown("""
<style>
/* Base reset e tipografia acadêmica */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Raleway:wght@300;400;500&display=swap');

:root {
    --primary-dark: #003366;
    --primary-light: #4a6fa5;
    --secondary-dark: #5c2018;
    --secondary-light: #bc4639;
    --text-dark: #333333;
    --text-light: #5a5a5a;
    --bg-light: #f8f9fa;
    --highlight: #d4a59a;
}

#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

.block-container {
    padding-top: 70px !important;
    font-family: 'Raleway', sans-serif;
    color: var(--text-dark);
    line-height: 1.6;
}

/* Barra de navegação premium */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    height: 70px;
    background: white;
    border-bottom: 1px solid rgba(0, 51, 102, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 5%;
    z-index: 1000;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
    font-family: 'Playfair Display', serif;
}

.nav-container {
    width: 100%;
    max-width: 1200px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo-container {
    display: flex;
    align-items: baseline;
    padding: 10px 0;
}

.logo-main {
    font-weight: 700;
    font-size: 28px;
    color: var(--primary-dark);
    letter-spacing: 0.5px;
    position: relative;
}

.logo-main::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--secondary-light);
}

.logo-sub {
    font-family: 'Raleway', sans-serif;
    font-weight: 400;
    font-size: 14px;
    color: var(--text-light);
    margin-left: 10px;
    letter-spacing: 1px;
}

/* Itens de navegação */
.nav-items {
    display: flex;
    gap: 30px;
}

.nav-item {
    position: relative;
}

.nav-link {
    color: var(--text-dark);
    font-weight: 500;
    font-size: 16px;
    padding: 25px 0;
    text-decoration: none;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
    position: relative;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: 20px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--secondary-light);
    transition: width 0.3s ease;
}

.nav-link:hover {
    color: var(--secondary-dark);
}

.nav-link:hover::after {
    width: 100%;
}

.has-dropdown .nav-link {
    display: flex;
    align-items: center;
    gap: 6px;
}

.dropdown-icon {
    transition: transform 0.3s ease;
}

.has-dropdown:hover .dropdown-icon {
    transform: rotate(180deg);
}

/* Dropdown menu */
.dropdown-content {
    position: absolute;
    top: 70px;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    min-width: 200px;
    padding: 15px 0;
    display: none;
    border-radius: 4px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    z-index: 1001;
}

.has-dropdown:hover .dropdown-content {
    display: block;
    animation: fadeIn 0.3s ease;
}

.dropdown-content a {
    color: var(--text-light);
    padding: 12px 20px;
    display: block;
    transition: all 0.3s ease;
    font-size: 15px;
    position: relative;
}

.dropdown-content a::before {
    content: '';
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--primary-light);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.dropdown-content a:hover {
    color: var(--primary-dark);
    background: rgba(74, 111, 165, 0.05);
    padding-left: 30px;
}

.dropdown-content a:hover::before {
    opacity: 1;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}

/* Destaque para seção atual */
.active .nav-link {
    color: var(--secondary-dark);
    font-weight: 600;
}

.active .nav-link::after {
    width: 100%;
}
</style>

<div class="navbar">
    <div class="nav-container">
        <div class="logo-container">
            <div class="logo-main">RMC</div>
            <div class="logo-sub">Região Metropolitana de Campinas</div>
        </div>
        
        <div class="nav-items">
            <div class="nav-item active">
                <a href="#" class="nav-link">Início</a>
            </div>
            
            <div class="nav-item has-dropdown">
                <a href="#" class="nav-link">
                    Economia
                    <svg class="dropdown-icon" width="12" height="7" viewBox="0 0 12 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 1L6 6L11 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </a>
                <div class="dropdown-content">
                    <a href="#">PIB Municipal</a>
                    <a href="#">PIB per capita</a>
                    <a href="#">Valor Adicionado Bruto</a>
                </div>
            </div>
            
            <div class="nav-item has-dropdown">
                <a href="#" class="nav-link">
                    Finanças
                    <svg class="dropdown-icon" width="12" height="7" viewBox="0 0 12 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 1L6 6L11 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </a>
                <div class="dropdown-content">
                    <a href="#">Orçamento Público</a>
                    <a href="#">Tributos Municipais</a>
                    <a href="#">Despesas por Setor</a>
                </div>
            </div>
            
            <div class="nav-item has-dropdown">
                <a href="#" class="nav-link">
                    Segurança
                    <svg class="dropdown-icon" width="12" height="7" viewBox="0 0 12 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 1L6 6L11 1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </a>
                <div class="dropdown-content">
                    <a href="#">Indicadores de Segurança</a>
                    <a href="#">Mapa de Ocorrências</a>
                    <a href="#">Dados Comparativos</a>
                </div>
            </div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">Publicações</a>
            </div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">Contato</a>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Conteúdo acadêmico de exemplo
st.markdown("""
<div style="max-width: 1000px; margin: 0 auto; padding: 20px;">
    <h1 style="font-family: 'Playfair Display', serif; color: #003366; border-bottom: 2px solid #bc4639; padding-bottom: 10px; margin-top: 40px;">
        Sistema de Dados Regionais - RMC
    </h1>
    
    <p style="font-size: 18px; margin-top: 30px;">
        Bem-vindo ao portal de dados científicos da Região Metropolitana de Campinas. 
        Esta plataforma oferece acesso a indicadores econômicos, financeiros e de 
        segurança pública, consolidando informações de 20 municípios da região.
    </p>
    
    <div style="margin-top: 50px; background: #f8f9fa; padding: 30px; border-left: 4px solid #4a6fa5;">
        <h3 style="color: #5c2018; margin-top: 0;">Sobre o Projeto</h3>
        <p>
            Desenvolvido em parceria com instituições de pesquisa, o RMC Data tem como 
            objetivo democratizar o acesso a dados regionais, fornecendo análises 
            precisas e visualizações interativas para pesquisadores, gestores públicos 
            e cidadãos.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
