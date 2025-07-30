import streamlit as st

pages = {
    st.Page("paginas/inicio.py", title="Início"),

    "Sobre": [
        st.Page("paginas/projeto.py", title="Projeto de Pesquisa"),
        st.Page("paginas/equipe.py", title="Equipe"),
    ],
    "Dados e Resultados": [
        st.Page("paginas/metodologia.py", title="Metodologia"),
        st.Page("paginas/municipais.py", title="Dispêndios Municipais"),
        st.Page("paginas/estaduais.py", title="Dispêndios Estaduais"),
        st.Page("paginas/documentos.py", title="Referências e Documentos"),
    ],
}

pg = st.navigation(pages)
pg.run()
