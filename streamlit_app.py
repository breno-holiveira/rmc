import streamlit as st

st.set_page_config(layout="wide")
st.markdown("<style>div[data-testid='stSidebar']{display:none !important;}</style>", unsafe_allow_html=True)

tabs = st.tabs(["Início", "Página 1", "Página 2"])

with tabs[0]:
    st.title("Início")
    st.write("Conteúdo da página inicial.")

with tabs[1]:
    st.title("Página 1")
    st.write("Conteúdo da página 1.")

with tabs[2]:
    st.title("Página 2")
    st.write("Conteúdo da página 2.")
