import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Captura da página via URL
params = st.query_params
page = params.get("page", "inicio")

# Estilo visual institucional refinado
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&display=swap');

body {
    font-family: 'Playfair Display', serif;
}

#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

.block-container {
    padding-top: 72px !important;
}

/* NAVBAR */
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 72px;
    background: #ffffff;
    border-bottom: 1px solid #dee2e6;
    display: flex;
    align-items: center;
    padding: 0 50px;
    gap: 40px;
    font-family: 'Playfair Display', serif;
    z-index: 9999;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

/* LOGO */
.logo {
    font-size: 26px;
    font-weight: 700;
    color: #1a2d40;
    margin-right: auto;
}

/* ITEM MENU */
.nav-item {
    position: relative;
}
.nav-link {
    color: #1a2d40;
    font-size: 18px;
    text-decoration: none;
    padding: 8px 10px;
    display: inline-block;
    transition: 0.2s;
}
.nav-link:hover {
    color: #0a58ca;
}

/* DROPDOWN */
.dropdown-content {
    display: none;
    position: absolute;
    background-color: #ffffff;
    top: 48px;
    min-width: 200px;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    border-radius: 6px;
    z-index: 9999;
    border-top: 3px solid #0a58ca;
}
.nav-item:hover .dropdown-content {
    display: block;
}
.dropdown-content a {
    color: #1a2d40;
    padding: 10px 20px;
    display: block;
    text-decoration: none;
    font-size: 16px;
}
.dropdown-content a:hover {
    background-color: #f1f1f1;
    color: #0a58ca;
}
</style>

<!-- HTML da Navbar -->
<div class="navbar">
  <div class="logo">RMC Data</div>

  <div class="nav-item">
    <a class="nav-link" href="/?page=inicio">Início</a>
  </div>

  <div class="nav-item">
    <span class="nav-link">Economia ▼</span>
    <div class="dropdown-content">
      <a href="/?page=pib">PIB Municipal</a>
      <a href="/?page=pib_per_capita">PIB per capita</a>
      <a href="/?page=vab">Valor Adicionado Bruto</a>
    </div>
  </div>

  <div class="nav-item">
    <span class="nav-link">Finanças ▼</span>
    <div class="dropdown-content">
      <a href="/?page=orcamento">Orçamento</a>
      <a href="/?page=tributos">Tributos</a>
      <a href="/?page=despesas">Despesas</a>
    </div>
  </div>

  <div class="nav-item">
    <span class="nav-link">Segurança ▼</span>
    <div class="dropdown-content">
      <a href="/?page=seguranca">Indicadores</a>
      <a href="/?page=mapa">Mapa de Ocorrências</a>
      <a href="/?page=comparativos">Comparativos</a>
    </div>
  </div>

  <div class="nav-item">
    <a class="nav-link" href="/?page=contato">Contato</a>
  </div>
</div>
""", unsafe_allow_html=True)

# Conteúdo baseado na navegação
match page:
    case "inicio":
        st.title("Bem-vindo ao RMC Data")
        st.write("Este é o portal de dados científicos da Região Metropolitana de Campinas.")
    case "pib":
        st.title("PIB Municipal")
        st.write("Página com dados de Produto Interno Bruto dos municípios.")
    case "pib_per_capita":
        st.title("PIB per capita")
    case "vab":
        st.title("Valor Adicionado Bruto")
    case "orcamento":
        st.title("Orçamento Público")
    case "tributos":
        st.title("Tributos Municipais")
    case "despesas":
        st.title("Despesas por Setor")
    case "seguranca":
        st.title("Indicadores de Segurança")
    case "mapa":
        st.title("Mapa de Ocorrências")
    case "comparativos":
        st.title("Dados Comparativos")
    case "contato":
        st.title("Fale Conosco")
        st.write("Entre em contato com a equipe do RMC Data.")
    case _:
        st.title("Página não encontrada")
