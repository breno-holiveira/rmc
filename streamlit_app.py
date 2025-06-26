import streamlit as st

st.set_page_config(layout="wide")
st.markdown("<style>div[data-testid='stSidebar']{display:none !important;}</style>", unsafe_allow_html=True)

page = st.select_slider(
    "Selecione a página:",
    options=["Início", "Página 1", "Página 2"],
    value="Início"
)

st.write(f"Você está na página: **{page}**")

if page == "Início":
    st.write("Conteúdo da página inicial.")
elif page == "Página 1":
    st.write("Conteúdo da página 1.")
else:
    st.write("Conteúdo da página 2.")
