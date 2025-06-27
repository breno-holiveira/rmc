import streamlit as st

st.set_page_config(page_title='RMC Data', layout='wide')

# Inicializa
if "page" not in st.session_state:
    st.session_state.page = "inicio"

# Função para mudar de página
def mudar_pagina(p):
    st.session_state.page = p

# Estilo + HTML da navbar
st.markdown("""
<style>
.navbar {
    background-color: #0B1D3A;
    padding: 1rem;
    display: flex;
    gap: 1rem;
}
.nav-link {
    color: #E0E6F0;
    background: none;
    border: none;
    font-size: 14px;
    padding: 8px 16px;
    cursor: pointer;
}
.nav-link:hover {
    background-color: #1F355A;
    color: white;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# Barra com botões (em linha)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("Início", key="inicio", help="Página inicial", use_container_width=True):
        mudar_pagina("inicio")
with col2:
    if st.button("Sobre", key="sobre", use_container_width=True):
        mudar_pagina("sobre")
with col3:
    if st.button("Economia", key="economia", use_container_width=True):
        mudar_pagina("economia")
with col4:
    if st.button("Finanças", key="financas", use_container_width=True):
        mudar_pagina("financas")
with col5:
    if st.button("Despesas", key="despesas", use_container_width=True):
        mudar_pagina("despesas")
with col6:
    if st.button("Arrecadação", key="arrecadacao", use_container_width=True):
        mudar_pagina("arrecadacao")

# Conteúdo das páginas
st.markdown("<br>", unsafe_allow_html=True)
if st.session_state.page == "inicio":
    st.title("Início")
    st.write("Bem-vindo ao Sistema RMC Data.")
elif st.session_state.page == "sobre":
    st.title("Sobre")
    st.write("Informações sobre o projeto.")
elif st.session_state.page == "economia":
    st.title("Economia")
    st.write("Dados econômicos regionais.")
elif st.session_state.page == "financas":
    st.title("Finanças")
    st.write("Informações financeiras gerais.")
elif st.session_state.page == "despesas":
    st.title("Finanças > Despesas")
    st.write("Despesas públicas da RMC.")
elif st.session_state.page == "arrecadacao":
    st.title("Finanças > Arrecadação")
    st.write("Receita e arrecadação dos municípios.")
else:
    st.warning("Página não encontrada.")
