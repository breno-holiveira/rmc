import streamlit as st

st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# Página atual (via parâmetro da URL)
pagina = st.query_params.get("page", ["inicio"])[0]

# --- Classes 'active' para cada item ---
def ativa(p): return "nav-link active" if pagina == p else "nav-link"

# --- HTML da barra, com classes dinâmicas injetadas ---
navbar_html = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Raleway:wght@300;400;500&display=swap');

:root {{
  --primary-dark: #003366;
  --primary-light: #4a6fa5;
  --secondary-dark: #5c2018;
  --secondary-light: #bc4639;
  --text-dark: #333333;
  --text-light: #5a5a5a;
}}

#MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
  display: none !important;
}}

.block-container {{
  padding-top: 70px !important;
  font-family: 'Raleway', sans-serif;
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
        <a href="?page=inicio" class="{ativa('inicio')}">Início</a>
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
        <a href="?page=publicacoes" class="{ativa('publicacoes')}">Publicações</a>
      </div>

      <div class="nav-item">
        <a href="?page=contato" class="{ativa('contato')}">Contato</a>
      </div>
    </div>
  </div>
</div>
"""

# Renderiza o HTML e CSS
st.markdown(navbar_html, unsafe_allow_html=True)

# Nenhum conteúdo abaixo (como solicitado)
