import streamlit as st

st.set_page_config(page_title="Teste Navegação", layout="wide")

# Remove sidebar
st.markdown("""
<style>
div[data-testid="stSidebar"] {display:none !important;}
</style>
""", unsafe_allow_html=True)

params = st.query_params
page = params.get("page", ["home"])[0]

menu_items = {
    "Início": "home",
    "Página 1": "pag1",
    "Página 2": "pag2",
}

menu_html = '<div style="background:#ff6600; padding:10px; font-weight:bold;">'
for label, p in menu_items.items():
    color = "white" if page == p else "rgba(255,255,255,0.7)"
    menu_html += f'<a href="?page={p}" style="margin:10px; color:{color}; text-decoration:none;">{label}</a>'
menu_html += '</div>'

st.markdown(menu_html, unsafe_allow_html=True)

st.write(f"Você está na página: **{page}**")
