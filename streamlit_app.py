import streamlit as st

st.set_page_config(layout="wide")
st.markdown("<style>div[data-testid='stSidebar']{display:none !important;}</style>", unsafe_allow_html=True)

page = st.selectbox("Selecione a página", ["Início", "Página 1", "Página 2"])

if page == "Início":
    st.title("Início")
    st.write("Conteúdo da página inicial.")

elif page == "Página 1":
    st.title("Página 1")
    st.write("Conteúdo da página 1.")

else:
    st.title("Página 2")
    st.write("Conteúdo da página 2.")
