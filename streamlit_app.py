import streamlit as st

st.set_page_config(page_title="App com Navbar", layout="wide", initial_sidebar_state="collapsed")

# Simula o navbar com st.radio horizontal
st.markdown("""
    <style>
        .navbar-container {
            background-color: rgb(123, 209, 146);
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            justify-content: center;
        }

        .navbar-container label {
            background-color: rgba(255, 255, 255, 0.15);
            color: rgb(49, 51, 63);
            border-radius: 0.5rem;
            margin: 0 0.25rem;
            padding: 0.4rem 0.75rem;
            transition: background-color 0.3s ease;
            cursor: pointer;
        }

        .navbar-container input:checked + div {
            background-color: rgba(255, 255, 255, 0.35) !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Cria o "navbar"
pages = ["Home", "Library", "Tutorials", "Development", "Download"]
selected = st.radio("",
    pages,
    horizontal=True,
    key="main_nav",
    label_visibility="collapsed"
)

# Conteúdo condicional da página
st.write(f"Você está na página: **{selected}**")

# Sidebar opcional
with st.sidebar:
    st.write("Sidebar aqui")
