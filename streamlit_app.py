import streamlit as st

import pages.inicio as inicio
import pages.despesas as despesas
import pages.receitas as receitas
import pages.emprego_renda as emprego_renda
import pages.precos as precos
import pages.producao as producao
import pages.balanca_comercial as balanca_comercial
import pages.acidentes_transito as acidentes_transito
import pages.taxa_homicidios as taxa_homicidios
import pages.alertas as alertas
import pages.contato as contato

st.set_page_config(
    page_title="RMC Data",
    layout="wide",
    initial_sidebar_state="collapsed"
)

params = st.query_params
pagina = params.get("page", "inicio")

st.markdown("""
<style>
    * {
        font-family: Arial, Helvetica, sans-serif !important;
    }

    /* Oculta elementos do Streamlit */
    #MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    .block-container {
        padding-top: 60px !important;
    }

    /* Navbar */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 54px;
        background: #ffffff;
        border-bottom: 1px solid #cccccc;
        display: flex;
        align-items: center;
        padding: 0 32px;
        gap: 32px;
        z-index: 9999;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    /* Logo maior, refinada e centralizada verticalmente */
    .logo-container {
        display: flex;
        align-items: center;
        font-family: 'Times', serif;
        font-size: 36px;
        font-weight: 600;
        color: #1f1e1e;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        margin-right: auto;
        user-select: none;
        position: relative;
        padding-bottom: 0;
    }

    .logo-container .highlight {
        font-size: 32px;
        font-weight: 600;
        color: #2f5e88;
        margin-left: 8px;
        font-variant: small-caps;
        letter-spacing: 0.02em;
        text-transform: none;
        line-height: 1;
    }

    .nav-item {
        position: relative;
        cursor: pointer;
    }

    .nav-link, a.nav-link {
        color: #222;
        font-size: 17px;
        padding: 14px 10px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        transition: color 0.3s ease;
        border-radius: 4px;
        font-weight: 500;
    }

    .nav-link:hover, a.nav-link:hover,
    .nav-item:hover > .nav-link {
        color: #1a3e66;
    }

    .dropdown-arrow {
        margin-left: 6px;
        border: solid #444;
        border-width: 0 2px 2px 0;
        display: inline-block;
        padding: 3px;
        transform: rotate(45deg);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }

    .nav-item:hover .dropdown-arrow {
        transform: rotate(225deg);
        border-color: #1a3e66;
    }

    .dropdown-content {
        position: absolute;
        top: 54px;
        left: 0;
        background: #ffffff;
        min-width: 190px;
        border-top: 3px solid #2f5e88;
        padding: 8px 0;
        display: none;
        border-radius: 0 0 8px 8px;
        z-index: 99999;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.1);
    }

    .nav-item:hover .dropdown-content {
        display: block;
    }

    .dropdown-content a {
        color: #222;
        padding: 10px 22px;
        font-size: 17px;
        text-decoration: none;
        display: block;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .dropdown-content a:hover {
        color: #1a3e66;
        padding-left: 28px;
    }
</style>

<!-- HTML da BARRA DE NAVEGAÇÃO -->
<div class="navbar">
    <div class="logo-container">RMC<span class="highlight">Data</span></div>
    <div class="nav-item">
        <a href="/?page=inicio" class="nav-link" target="_self">Início</a>
    </div>
    <div class="nav-item">
        <span class="nav-link">Economia <span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="/?page=emprego_renda" target="_self">Emprego e renda</a>
            <a href="/?page=precos" target="_self">Preços</a>
            <a href="/?page=producao" target="_self">Produção</a>
        </div>
    </div>
    <div class="nav-item">
        <span class="nav-link">Finanças<span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="/?page=balanca_comercial" target="_self">Balança comercial</a>
            <a href="/?page=despesas" target="_self">Despesas</a>
            <a href="/?page=receitas" target="_self">Receitas</a>
        </div>
    </div>
    <div class="nav-item">
        <span class="nav-link">Segurança <span class="dropdown-arrow"></span></span>
        <div class="dropdown-content">
            <a href="/?page=taxa_homicidios" target="_self">Taxa de homicídios</a>
            <a href="/?page=acidentes_transito" target="_self">Acidentes de trânsito</a>
        </div>
    </div>
    <div class="nav-item">
        <a href="/?page=contato" class="nav-link" target="_self">Contato</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Roteamento
match pagina:
    case "inicio":
        inicio.show()
    case "despesas":
        despesas.show()
    case "receitas":
        receitas.show()
    case "emprego_renda":
        emprego_renda.show()
    case "precos":
        precos.show()
    case "balanca_comercial":
        balanca_comercial.show()
    case "acidentes_transito":
        acidentes_transito.show()
    case "taxa_homicidios":
        taxa_homicidios.show()
    case "alertas":
        alertas.show()
    case "producao":
        producao.show()
    case "contato":
        contato.show()
    case _:
        st.warning("Página não encontrada.")
