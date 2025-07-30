import streamlit as st

pages = {
    "Sobre": [
        st.Page("teste1.py", title="Projeto de Pesquisa"),
        st.Page("teste2.py", title="Equipe"),
    ],
    "Dados e Resultados": [
        st.Page("teste3.py", title="Metodologia"),
        st.Page("teste4.py", title="Dados Municipais"),
        st.Page("teste5.py", title="Dados Estaduais"),
    ],
}

pg = st.navigation(pages)
pg.run()
