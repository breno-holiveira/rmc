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
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    /* Oculta elementos do Streamlit */
    #MainMenu, footer, header, [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }

    .block-container {
        padding-top: 64px !important;
    }

    /* Navbar */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 56px;
        background: #fdfdfd;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        align-items: center;
        padding: 0 36px;
        gap: 28px;
        z-index: 9999;
        box-shadow: 0 1px 6px rgba(0,0,0,0.03);
    }

    /* Logo refinada */
    .logo-container {
        display: flex;
        align-items: baseline;
        font-family: 'Georgia', serif;
        font-size: 30px;
        font-weight: 600;
        color: #242424;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        margin-right: auto;
        user-select: none;
    }

    .logo-separator {
        display: inline-block;
        width: 6px;
        height: 6px;
        background: #264a73;
        border-radius: 50%;
        margin: 0 8px;
        transform: translateY(-2px);
    }

    .logo-highlight {
        font-size: 24px;
        font-weight: 400;
        color: #264a73;
        font-variant: small-caps;
        font-style: italic;
        opacity: 0.9;
        letter-spacing: 0.03em;
    }

    /* Navegação */
    .nav-item {
        position: relative;
        cursor: pointer;
    }

    .nav-link, a.nav-link {
        color: #333;
        font-size: 16px;
        padding: 12px 10px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .nav-link:hover,
    a.nav-link:hover,
    .nav-item:hover > .nav-link {
        color: #1e3f66;
    }

    .dropdown-arrow {
        margin-left: 6px;
        border: solid #555;
        border-width: 0 2px 2px 0;
        padding: 3px;
        transform: rotate(45deg);
        transition: transform 0.3s ease;
    }

    .nav-item:hover .dropdown-arrow {
        transform: rotate(225deg);
    }

    .dropdown-content {
        position: absolute;
        top: 56px;
        left: 0;
        background: #ffffff;
        min-width: 180px;
        border-top: 3px solid #264a73;
        padding: 6px 0;
        display: none;
        border-radius: 0 0 8px 8px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
        z-index: 99999;
    }

    .nav-item:hover .dropdown-content {
        display: block;
    }

    .dropdown-content a {
        color: #333;
        padding: 10px 20px;
        font-size: 15.5px;
        text-decoration: none;
        display: block;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .dropdown-content a:hover {
        background-color: #f5f5f5;
        color: #1e3f66;
        padding-left: 28px;
    }
</style>

<!-- HTML da barra -->
<div class="navbar">
    <div class="logo-container">
        RMC<span class="logo-separator"></span><span class="logo-highlight">Data</span>
    </div>

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
        <span class="nav-link">Finanças <span class="dropdown-arrow"></span></span>
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
