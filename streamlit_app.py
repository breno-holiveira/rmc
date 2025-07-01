import streamlit as st

# Configuração da página com rigor científico
st.set_page_config(
    page_title="RMC Data | Painel Estatístico Oficial",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📈"
)

# CSS Premium com tipografia acadêmica
st.markdown("""
<style>
/* Fonte principal: IBM Plex Sans (usada pela OCDE e ONU) */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --oxford-blue: #002147;
    --prussian-blue: #003153;
    --dark-slate: #2F4F4F;
    --cadet-gray: #91A3B0;
    --ivory: #FFFFF0;
    --alabaster: #F2F0E6;
}

#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

/* Container principal */
.block-container {
    padding-top: 85px !important;
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--oxford-blue);
    line-height: 1.7;
}

/* Barra de Navegação Científica */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    height: 85px;
    background: var(--ivory);
    border-bottom: 1px solid rgba(0, 33, 71, 0.15);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 33, 71, 0.08);
}

.nav-container {
    width: 100%;
    max-width: 1400px;
    padding: 0 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Logotipo Científico */
.logo-scientific {
    display: flex;
    align-items: baseline;
    font-family: 'IBM Plex Sans', sans-serif;
}

.logo-main {
    font-weight: 700;
    font-size: 28px;
    color: var(--oxford-blue);
    letter-spacing: -0.5px;
}

.logo-sub {
    font-weight: 400;
    font-size: 16px;
    color: var(--dark-slate);
    margin-left: 12px;
    position: relative;
    top: -2px;
}

.logo-divider {
    color: var(--cadet-gray);
    margin: 0 8px;
    font-weight: 300;
}

/* Navegação Acadêmica */
.nav-items {
    display: flex;
    gap: 12px;
}

.nav-item {
    position: relative;
    padding: 0 5px;
}

.nav-link {
    color: var(--oxford-blue);
    font-weight: 500;
    font-size: 15px;
    padding: 30px 15px;
    text-decoration: none;
    letter-spacing: 0.3px;
    position: relative;
    transition: color 0.25s ease;
}

.nav-link:hover {
    color: var(--prussian-blue);
}

.nav-link:after {
    content: '';
    position: absolute;
    bottom: 25px;
    left: 15px;
    width: calc(100% - 30px);
    height: 2px;
    background: var(--prussian-blue);
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s ease;
}

.nav-link:hover:after {
    transform: scaleX(1);
    transform-origin: left;
}

/* Dropdown Científico */
.dropdown-content {
    position: absolute;
    top: 82px;
    left: 0;
    background: var(--ivory);
    min-width: 220px;
    padding: 12px 0;
    opacity: 0;
    visibility: hidden;
    border-radius: 0 0 4px 4px;
    box-shadow: 0 12px 24px rgba(0, 33, 71, 0.15);
    z-index: 1001;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.1);
    transform: translateY(10px);
    border-top: 3px solid var(--prussian-blue);
}

.nav-item:hover .dropdown-content {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.dropdown-content a {
    color: var(--dark-slate);
    padding: 12px 24px;
    font-size: 14.5px;
    display: flex;
    align-items: center;
    transition: all 0.2s ease;
    border-left: 3px solid transparent;
}

.dropdown-content a:before {
    content: '→';
    margin-right: 12px;
    font-size: 12px;
    color: var(--cadet-gray);
    transition: all 0.2s ease;
}

.dropdown-content a:hover {
    background: rgba(0, 49, 83, 0.03);
    color: var(--prussian-blue);
    border-left: 3px solid var(--prussian-blue);
    padding-left: 28px;
}

.dropdown-content a:hover:before {
    color: var(--prussian-blue);
    margin-right: 15px;
}

/* Ícone de dropdown científico */
.dropdown-icon {
    display: inline-flex;
    margin-left: 6px;
    transition: all 0.3s ease;
}

.nav-item:hover .dropdown-icon {
    transform: rotate(180deg);
}
</style>

<!-- Template HTML -->
<div class="navbar">
    <div class="nav-container">
        <div class="logo-scientific">
            <div class="logo-main">RMC</div>
            <span class="logo-divider">|</span>
            <div class="logo-sub">Observatório de Dados Regionais</div>
        </div>
        
        <div class="nav-items">
            <div class="nav-item">
                <a href="#" class="nav-link">Painel Estatístico</a>
            </div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">
                    Indicadores Econômicos
                    <span class="dropdown-icon">▼</span>
                </a>
                <div class="dropdown-content">
                    <a href="#">Produto Interno Bruto</a>
                    <a href="#">PIB Per Capita</a>
                    <a href="#">Valor Adicionado Bruto</a>
                    <a href="#">Índices de Produtividade</a>
                </div>
            </div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">
                    Finanças Públicas
                    <span class="dropdown-icon">▼</span>
                </a>
                <div class="dropdown-content">
                    <a href="#">Orçamento Municipal</a>
                    <a href="#">Receitas Tributárias</a>
                    <a href="#">Despesas por Função</a>
                </div>
            </div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">
                    Segurança Urbana
                    <span class="dropdown-icon">▼</span>
                </a>
                <div class="dropdown-content">
                    <a href="#">Mapa Criminal</a>
                    <a href="#">Estatísticas Comparativas</a>
                </div>
            </div>
            
            <div class="nav-item">
                <a href="#" class="nav-link">Publicações Técnicas</a>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Conteúdo Científico
st.markdown("""
<div style="max-width: 1200px; margin: 0 auto; padding: 40px 20px;">
    <h1 style="font-weight:600; color:#002147; border-bottom:2px solid #003153; padding-bottom:12px; margin-bottom:30px;">
        PAINEL ESTATÍSTICO OFICIAL - REGIÃO METROPOLITANA DE CAMPINAS
    </h1>
    
    <div style="background:#F8F9FA; padding:30px; margin-bottom:40px; border-left:4px solid #003153;">
        <p style="font-size:17px; line-height:1.8; color:#2F4F4F;">
            <strong>Sistema de Informação Georreferenciada</strong> | Este portal consolida dados oficiais da 
            Região Metropolitana de Campinas, fornecendo análises técnicas e indicadores 
            validados por órgãos competentes. Todas as séries históricas seguem metodologias 
            reconhecidas pelo IBGE e FGV.
        </p>
    </div>
    
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(350px, 1fr)); gap:30px; margin-top:50px;">
        <div style="background:white; padding:25px; box-shadow:0 4px 20px rgba(0,0,0,0.05); border-top:3px solid #003153;">
            <h3 style="color:#002147; margin-top:0;">Dados Estruturais</h3>
            <p style="color:#5F6C72; line-height:1.7;">
                Séries históricas comparativas entre os 20 municípios da RMC, com taxas 
                anuais de crescimento desde 2010.
            </p>
        </div>
        
        <div style="background:white; padding:25px; box-shadow:0 4px 20px rgba(0,0,0,0.05); border-top:3px solid #003153;">
            <h3 style="color:#002147; margin-top:0;">Metodologia Científica</h3>
            <p style="color:#5F6C72; line-height:1.7;">
                Documentação técnica completa sobre coleta, processamento e validação 
                dos dados, com referências bibliográficas.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
