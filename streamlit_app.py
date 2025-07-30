import streamlit as st

pages = {
    "Início": [
        st.Page("teste1.py", title="Teste 1"),
        st.Page("teste2.py", title="Teste 2"),
    ],
    "Sobre": [
        st.Page("teste3.py", title="Teste 3"),
        st.Page("teste4.py", title="Teste 4"),
    ],
}

pg = st.navigation(pages)
pg.run()
