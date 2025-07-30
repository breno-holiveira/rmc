import streamlit as st

pages = {
    "Início": [
        st.Page("projeto.py", title="Projeto de Pesquisa"),
        st.Page("integrantes.py", title="Integrantes"),
    ],
    "Dados e Resultados": [
        st.Page("metodologia.py", title="Metodologia"),
        st.Page("municipais.py", title="Dispêndios Municipais em C&T"),
        st.Page("estaduais.py", title="Dispêndios Estaduais em C&T"),
        st.Page("documentos.py", title="Referências e Documentos"),
    ],
}

pg = st.navigation(pages)
pg.run()
