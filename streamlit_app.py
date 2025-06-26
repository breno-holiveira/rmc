import streamlit as st

st.set_page_config(page_title="Menu Simples", layout="wide")

# Remove barra lateral
st.markdown("""
<style>
div[data-testid="stSidebar"] {display:none !important;}
/* Container principal ocupa 100% */
div[data-testid="stAppViewContainer"] > .main > div:first-child {
    max-width: 100% !important;
    padding-left: 1rem !important;
}

/* Menu fixo no topo */
.menu {
    position: fixed;
    top: 0; left: 0; right: 0;
    background-color: #f63366;  /* cor laranja padrão Streamlit */
    display: flex;
    padding: 0.5rem 2rem;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    font-weight: 600;
    font-size: 1.05rem;
    z-index: 9999;
}

/* Links do menu */
.menu a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1.1rem;
    margin-right: 0.8rem;
    border-radius: 6px;
    transition: background-color 0.3s ease;
}

/* Hover */
.menu a:hover {
    background-color: rgba(255,255,255,0.3);
}

/* Link ativo */
.menu a.active {
    background-color: rgba(255,255,255,0.5);
    box-shadow: 0 0 8px rgba(255,255,255,0.7);
}

/* Conteúdo com espaçamento para não ficar por baixo do menu */
.content {
    padding-top: 60px;
    max-width: 1100px;
    margin: 1rem auto 2rem auto;
}
</style>
""", unsafe_allow_html=True)

# Lê parâmetro page
params = st.query_params
page = params.get("page", ["home"])[0]

# Menu items
menu_items = {
    "Início": "home",
    "Página 1": "pag1",
    "Página 2": "pag2",
    "Página 3": "pag3",
}

# Monta menu HTML
menu_html = '<div class="menu">'
for label, p in menu_items.items():
    active = "active" if page == p else ""
    menu_html += f'<a href="?page={p}" class="{active}">{label}</a>'
menu_html += '</div>'

st.markdown(menu_html, unsafe_allow_html=True)

# Conteúdo principal
st.markdown('<div class="content">', unsafe_allow_html=True)

if page == "home":
    st.title("Início")
    st.write("Conteúdo da página inicial aqui.")

elif page == "pag1":
    st.title("Página 1")
    st.write("Conteúdo da página 1 aqui.")

elif page == "pag2":
    st.title("Página 2")
    st.write("Conteúdo da página 2 aqui.")

elif page == "pag3":
    st.title("Página 3")
    st.write("Conteúdo da página 3 aqui.")

else:
    st.error("Página não encontrada.")

st.markdown('</div>', unsafe_allow_html=True)
