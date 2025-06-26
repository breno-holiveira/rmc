import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
div[data-testid="stSidebar"] {display:none !important;}
.fixed-menu {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: #f63366;
    padding: 12px 20px;
    display: flex;
    gap: 15px;
    font-weight: bold;
    font-family: Arial, sans-serif;
    z-index: 10000;
}
.fixed-menu button {
    background: transparent;
    border: none;
    color: white;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.3s ease;
}
.fixed-menu button:hover {
    background: rgba(255,255,255,0.3);
}
.fixed-menu button.active {
    background: rgba(255,255,255,0.6);
}
.content {
    padding-top: 60px;
    max-width: 900px;
    margin: 0 auto;
}
</style>

<div class="fixed-menu">
    <button id="btnHome">Início</button>
    <button id="btnPag1">Página 1</button>
    <button id="btnPag2">Página 2</button>
</div>

<script>
const buttons = document.querySelectorAll(".fixed-menu button");
buttons.forEach(btn => btn.addEventListener("click", () => {
    buttons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    window.parent.postMessage({func: 'setPage', page: btn.id}, '*');
}));
</script>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "btnHome"

def set_page(page_id):
    if page_id == "btnHome":
        st.session_state.page = "Início"
    elif page_id == "btnPag1":
        st.session_state.page = "Página 1"
    elif page_id == "btnPag2":
        st.session_state.page = "Página 2"

# Escuta mensagens JS - (obs: funciona somente local e em Streamlit sharing)
import streamlit.components.v1 as components

components.html(
    """
    <script>
    window.addEventListener('message', (event) => {
        if(event.data.func === 'setPage'){
            window.parent.postMessage({func:'pageChanged', page:event.data.page}, '*');
        }
    });
    </script>
    """,
    height=0,
)

st.write(f"Página atual: {st.session_state.page}")
