import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
div[data-testid="stSidebar"] {display:none !important;}
.menu {
    background:#f63366;
    padding:10px 30px;
    display:flex;
    gap:20px;
}
.menu a {
    color:white;
    text-decoration:none;
    font-weight:bold;
}
.menu a.active {
    text-decoration:underline;
}
</style>
""", unsafe_allow_html=True)

page = st.experimental_get_query_params().get("page", ["home"])[0]

menu = {
    "home": "Início",
    "pag1": "Página 1",
    "pag2": "Página 2",
}

menu_html = '<div class="menu">'
for key, label in menu.items():
    active = "active" if page == key else ""
    menu_html += f'<a href="?page={key}" class="{active}">{label}</a>'
menu_html += '</div>'

st.markdown(menu_html, unsafe_allow_html=True)

st.write(f"Você está na página: **{page}**")
