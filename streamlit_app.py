import streamlit as st

st.set_page_config(layout="wide")

# Oculta sidebar (mas deixa funcional)
st.markdown("""
<style>
[data-testid="stSidebar"] {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Escolha a página:", ["Início", "Página 1", "Página 2"])

st.write(f"Você está na página: **{page}**")

if page == "Início":
    st.write("Conteúdo da página inicial.")
elif page == "Página 1":
    st.write("Conteúdo da página 1.")
else:
    st.write("Conteúdo da página 2.")
