import streamlit as st

st.set_page_config(layout="wide")
st.markdown("<style>div[data-testid='stSidebar']{display:none !important;}</style>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

cols = st.columns([1,1,1])

with cols[0]:
    if st.button("Início"):
        st.session_state.page = "home"
with cols[1]:
    if st.button("Página 1"):
        st.session_state.page = "pag1"
with cols[2]:
    if st.button("Página 2"):
        st.session_state.page = "pag2"

if st.session_state.page == "home":
    st.title("Início")
    st.write("Conteúdo da página inicial.")
elif st.session_state.page == "pag1":
    st.title("Página 1")
    st.write("Conteúdo da página 1.")
else:
    st.title("Página 2")
    st.write("Conteúdo da página 2.")
