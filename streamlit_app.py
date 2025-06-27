import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="RMC Data", layout="wide", initial_sidebar_state="collapsed")

# Inicia a página padrão
if "page" not in st.session_state:
    st.session_state.page = "inicio"

# Controle de navegação via mensagem JS
components.html("""
<script>
function navigateTo(page) {
    const streamlitEvent = new CustomEvent("streamlit:message", {
        detail: { type: "streamlit:setComponentValue", key: "page", value: page }
    });
    window.parent.dispatchEvent(streamlitEvent);
}
</script>
""", height=0)

# HTML + CSS da navbar estilizada com dropdown
st.markdown("""
<style>
    .navbar {
        background-color: #0B1D3A;
        padding: 0 2rem;
        height: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: Arial, sans-serif;
    }
    .navbar-title {
        color: white;
        font-size: 22px;
        font-weight: bold;
        margin-right: 30px;
    }
    .nav-links {
        display: flex;
        gap: 0;
        height: 100%;
    }
    .nav-item {
        position: relative;
        height: 100%;
    }
    .nav-link {
        color: #E0E6F0;
        text-decoration: none;
        padding: 0 20px;
        height: 100%;
        display: flex;
        align-items: center;
        font-size: 14px;
        transition: all 0.1s ease;
        cursor: pointer;
    }
    .nav-link:hover {
        color: white;
        background-color: #1F355A;
    }
    .dropdown-content {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: #0B1D3A;
        min-width: 180px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
        display: none;
        border-top: 2px solid #2D4375;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    .dropdown-item {
        color: #E0E6F0;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        font-size: 13px;
        transition: all 0.1s ease;
        border-left: 3px solid transparent;
        cursor: pointer;
    }
    .dropdown-item:hover {
        background-color: #1F355A;
        border-left: 3px solid #4F46E5;
    }
</style>

<div class="navbar">
    <div class="navbar-title">RMC Data</div>
    <div class="nav-links">
        <div class="nav-item">
            <div class="nav-link" onclick="navigateTo('inicio')">Início</div>
        </div>
        <div class="nav-item">
            <div class="nav-link" onclick="navigateTo('sobre')">Sobre</div>
        </div>
        <div class="nav-item">
            <div class="nav-link" onclick="navigateTo('economia')">Economia</div>
        </div>
        <div class="nav-item dropdown">
            <div class="nav-link">Finanças</div>
            <div class="dropdown-content">
                <div class="dropdown-item" onclick="navigateTo('financas')">📊 Finanças</div>
                <div class="dropdown-item" onclick="navigateTo('despesas')">💸 Despesas</div>
                <div class="dropdown-item" onclick="navigateTo('arrecadacao')">💰 Arrecadação</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Atualiza a página com base na variável
page = st.session_state.page

# Conteúdo de cada "página"
if page == "inicio":
    st.title("Início")
    st.write("Bem-vindo ao RMC Data.")
elif page == "sobre":
    st.title("Sobre")
    st.write("Informações sobre o projeto.")
elif page == "economia":
    st.title("Economia")
    st.write("Dados econômicos da RMC.")
elif page == "financas":
    st.title("Finanças")
    st.write("Resumo financeiro.")
elif page == "despesas":
    st.title("Finanças > Despesas")
    st.write("Dados sobre despesas públicas.")
elif page == "arrecadacao":
    st.title("Finanças > Arrecadação")
    st.write("Informações sobre arrecadação municipal.")
else:
    st.warning("Página não encontrada.")
