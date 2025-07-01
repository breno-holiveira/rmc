import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# --- Lê a página atual a partir dos parâmetros da URL ---
query_params = st.query_params
pagina = query_params.get("page", ["inicio"])[0]

# --- CSS e HTML da navbar ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Raleway:wght@300;400;500&display=swap');

:root {{
    --primary-dark: #003366;
    --primary-light: #4a6fa5;
    --secondary-dark: #5c2018;
    --secondary-light: #bc4639;
    --text-dark: #333333;
    --text-light: #5a5a5a;
    --bg-light: #f8f9fa;
}}

#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
    display: none !important;
}}

.block-container {{
    padding-top: 70px !important;
    font-family: 'Raleway', sans-serif;
    color: var(--text-dark);
}}

.navbar {{
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
}}

.nav-container {{
    width: 100%;
    max-width: 1200px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo-container {{
    display: flex;
    align-items: baseline;
}}

.logo-main {{
    font-weight: 700;
    font-size: 28px;
    color: var(--primary-dark);
    position: relative;
}}

.logo-main::after {{
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--secondary-light);
}}

.logo-sub {{
    font-family: 'Raleway', sans-serif;
    font-weight: 400;
    font-size: 14px;
    color: var(--text-light);
    margin-left: 10px;
}}

.nav-items {{
    display: flex;
    gap: 30px;
}}

.nav-item {{
    position: relative;
}}

.nav-link {{
    color: var(--text-dark);
    font-weight: 500;
    font-size: 16px;
    padding: 25px 0;
    text-decoration: none;
    transition: all 0.3s ease;
}}

.nav-link:hover {{
    color: var(--secondary-dark);
}}

.nav-link.active {{
    color: var(--secondary-dark);
    font-weight: 600;
}}

.has-dropdown:hover .dropdown-content {{
    display: block;
}}

.dropdown-content {{
    position: absolute;
    top: 70px;
    left: 0;
    background: white;
    min-width: 200px;
    padding: 10px 0;
    display: none;
    border-radius: 4px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    z-index: 1001;
}}

.dropdown-content a {{
    color: var(--text-light);
    padding: 10px 20px;
    display: block;
    transition: all 0.3s ease;
}}

.dropdown-content a:hover {{
    color: var(--primary-dark);
    background: rgba(74, 111, 165, 0.05);
}}
</style>

<div class="navbar">
    <div class="nav-container">
        <div class="logo-container">
            <div class="logo-main">RMC</div>
            <div class="logo-sub">Região Metropolitana de Campinas</div>
        </div>
        
        <div class="nav-items">
            <div class="nav-item">
                <a href="?page=inicio" class="nav-link {'active' if pagina=='inicio' else ''}">Início</a>
            </div>
            
            <div class="nav-item has-dropdown">
                <a href="#" class="nav-link">Economia</a>
                <div class="dropdown-content">
                    <a href="?page=pib">PIB Municipal</a>
                    <a href="?page=pib_per_capita">PIB per capita</a>
                    <a href="?page=vab">Valor Adicionado Bruto</a>
                </div>
            </div>
            
            <div class="nav-item has-dropdown">
                <a href="#" class="nav-link">Finanças</a>
                <div class="dropdown-content">
                    <a href="?page=orcamento">Orçamento Público</a>
                    <a href="?page=tributos">Tributos Municipais</a>
                    <a href="?page=despesas">Despesas por Setor</a>
                </div>
            </div>
            
            <div class="nav-item has-dropdown">
                <a href="#" class="nav-link">Segurança</a>
                <div class="dropdown-content">
                    <a href="?page=seguranca">Indicadores de Segurança</a>
                    <a href="?page=mapa_ocorrencias">Mapa de Ocorrências</a>
                    <a href="?page=comparativos">Dados Comparativos</a>
                </div>
            </div>

            <div class="nav-item">
                <a href="?page=publicacoes" class="nav-link {'active' if pagina=='publicacoes' else ''}">Publicações</a>
            </div>
            
            <div class="nav-item">
                <a href="?page=contato" class="nav-link {'active' if pagina=='contato' else ''}">Contato</a>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Conteúdo dinâmico por página ---
if pagina == "inicio":
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

elif pagina == "pib":
    st.title("PIB Municipal")
    st.write("Conteúdo sobre o Produto Interno Bruto dos municípios da RMC.")

elif pagina == "pib_per_capita":
    st.title("PIB per capita")
    st.write("Conteúdo sobre o PIB per capita dos municípios da RMC.")

elif pagina == "vab":
    st.title("Valor Adicionado Bruto")
    st.write("Conteúdo sobre o VAB da RMC.")

elif pagina == "orcamento":
    st.title("Orçamento Público")
    st.write("Visualização e análise do orçamento público municipal.")

elif pagina == "tributos":
    st.title("Tributos Municipais")
    st.write("Análise de receitas tributárias nos municípios.")

elif pagina == "despesas":
    st.title("Despesas por Setor")
    st.write("Comparativo setorial dos gastos municipais.")

elif pagina == "seguranca":
    st.title("Indicadores de Segurança")
    st.write("Dados de criminalidade, policiamento e sensação de segurança.")

elif pagina == "mapa_ocorrencias":
    st.title("Mapa de Ocorrências")
    st.write("Visualização geográfica de ocorrências policiais.")

elif pagina == "comparativos":
    st.title("Dados Comparativos")
    st.write("Série histórica e análise entre os municípios.")

elif pagina == "publicacoes":
    st.title("Publicações")
    st.write("Artigos, relatórios e painéis publicados pela equipe.")

elif pagina == "contato":
    st.title("Contato")
    st.write("Informações para contato, equipe técnica e canais institucionais.")
