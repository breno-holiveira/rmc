import streamlit as st

pages = {
    "Sobre": [
        st.Page("projeto.py", title="Projeto de Pesquisa"),
        st.Page("integrantes.py", title="Integrantes"),
    ],
    "Dados e Resultados": [
        st.Page("metodologia.py", title="Metodologia"),
        st.Page("municipais.py", title="Dispêndios Municipais em C&T"),
        st.Page("estaduais.py", title="Dispêndios Estaduais em C&T"),
        st.Page("bibliografia.py", title="Bibliografia e Downloads de bibliografia e arquivos importantes"),
    ],
}

pg = st.navigation(pages)
pg.run()
