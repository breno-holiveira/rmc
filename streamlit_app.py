import streamlit as st

st.set_page_config(layout="wide")
st.markdown("<style>div[data-testid='stSidebar']{display:none !important;}</style>", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Início"

col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button("Início"):
        st.session_state.page = "Início"

with col2:
    if st.button("Página 1"):
        st.session_state.page = "Página 1"

with col3:
    if st.button("Página 2"):
        st.session_state.page = "Página 2"

st.write(f"Você está na página: **{st.session_state.page}**")

if st.session_state.page == "Início":
    st.write("Conteúdo da página inicial.")
elif st.session_state.page == "Página 1":
    st.write("Conteúdo da página 1.")
else:
    st.write("Conteúdo da página 2.")
