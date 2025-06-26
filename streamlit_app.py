import streamlit as st

# Configuração da página
st.set_page_config(page_title="RMC Navegação", layout="wide", page_icon="📊")

# --- CSS para barra de navegação moderna ---
st.markdown("""
    <style>
    .nav-container {
        background: #f0f2f6;
        border-bottom: 1px solid #ddd;
        padding: 10px 30px;
        display: flex;
        gap: 30px;
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    .nav-item {
        color: #444;
        text-decoration: none;
        padding-bottom: 3px;
        border-bottom: 2px solid transparent;
        transition: all 0.3s ease;
    }

    .nav-item:hover {
        border-bottom: 2px solid #8899aa;
        color: #2c3e70;
    }

    .nav-active {
        border-bottom: 2px solid #2c3e70;
        font-weight: 600;
        color: #2c3e70;
    }
    </style>
""", unsafe_allow_html=True)

# --- Função de navegação via query param ---
def navigation():
    try:
        return st.experimental_get_query_params().get('p', ['home'])[0]
    except:
        return 'home'

# --- Menu fixo personalizado ---
current = navigation()
menu_items = {
    "home": "Início",
    "results": "Resultados",
    "analysis": "Análise",
    "examples": "Exemplos",
    "logs": "Logs",
    "verify": "Verificação",
    "config": "Configurações"
}

menu_html = '<div class="nav-container">'
for key, label in menu_items.items():
    active = 'nav-active' if current == key else ''
    menu_html += f'<a class="nav-item {active}" href="/?p={key}">{label}</a>'
menu_html += '</div>'
st.markdown(menu_html, unsafe_allow_html=True)

# --- Conteúdo de cada página ---
if current == "home":
    st.title("🏠 Página Inicial")
    st.write("Bem-vindo à visualização de dados da Região Metropolitana de Campinas.")

elif current == "results":
    st.title("📋 Resultados")
    for item in range(25):
        st.write(f"Resultado {item+1}")

elif current == "analysis":
    st.title("📊 Análise de Dados")
    x = st.number_input("Digite X")
    y = st.number_input("Digite Y")
    st.success(f"Soma: {x + y}")

elif current == "examples":
    st.title("💡 Exemplos")
    st.info("Aqui você poderá explorar exemplos de uso do sistema.")

elif current == "logs":
    st.title("🗂 Logs")
    st.write("Exibição de logs completos.")

elif current == "verify":
    st.title("🔎 Verificação")
    st.warning("Verificando dados... aguarde.")

elif current == "config":
    st.title("⚙️ Configurações")
    st.write("Ajustes gerais do sistema.")

else:
    st.title("Página não encontrada")
    st.error("Verifique a URL ou selecione um item do menu.")
