import streamlit as st

st.set_page_config(page_title="Teste Navegação", layout="wide")

# Remove barra lateral
st.markdown("""
<style>
/* Remove sidebar */
div[data-testid="stSidebar"] {display:none !important;}
/* Ajusta o container principal para ocupar toda largura */
div[data-testid="stAppViewContainer"] > .main > div:first-child {
    max-width: 100% !important;
    padding-left: 1rem !important;
}

/* Barra fixa horizontal */
.navbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 52px;
    background-color: #ff6600;
    display: flex;
    align-items: center;
    padding: 0 30px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    z-index: 9999;
    box-shadow: 0 4px 8px rgba(255,102,0,0.3);
    user-select: none;
}

/* Itens do menu */
.navbar a {
    color: white;
    text-decoration: none;
    padding: 10px 18px;
    margin: 0 8px;
    border-radius: 8px;
    transition: background-color 0.3s ease;
}

/* Hover */
.navbar a:hover {
    background-color: rgba(255,255,255,0.3);
}

/* Item ativo */
.navbar a.active {
    background-color: #cc5200;
    box-shadow: 0 0 10px #cc5200;
}

/* Conteúdo com padding para não ficar por baixo da navbar */
.content {
    padding-top: 65px;
    max-width: 1200px;
    margin: 0 auto 2rem auto;
}
</style>
""", unsafe_allow_html=True)

# Lê parâmetro page da URL usando st.query_params
params = st.query_params
page = params.get("page", ["home"])[0]

# Menu com links (recarregam página com parâmetro ?page=xxx)
menu_items = {
    "Início": "home",
    "Página 1": "pag1",
    "Página 2": "pag2",
    "Página 3": "pag3",
}

# Monta HTML da navbar com destaque no ativo
menu_html = '<div class="navbar">\n'
for label, p in menu_items.items():
    active_class = "active" if page == p else ""
    menu_html += f'<a href="?page={p}" class="{active_class}">{label}</a>\n'
menu_html += '</div>'

st.markdown(menu_html, unsafe_allow_html=True)

# Conteúdo condicional
st.markdown('<div class="content">', unsafe_allow_html=True)

if page == "home":
    st.title("Início")
    st.write("Conteúdo da página inicial")

elif page == "pag1":
    st.title("Página 1")
    st.write("Conteúdo da página 1")

elif page == "pag2":
    st.title("Página 2")
    st.write("Conteúdo da página 2")

elif page == "pag3":
    st.title("Página 3")
    st.write("Conteúdo da página 3")

else:
    st.error("Página não encontrada")

st.markdown('</div>', unsafe_allow_html=True)
