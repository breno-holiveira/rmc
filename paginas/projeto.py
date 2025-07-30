import streamlit as st

st.markdown(
    """
    <h2 style='text-align: center;'>
        Dispêndio Público em Ciência e Tecnologia no Município de Campinas
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '''
    O projeto de pesquisa, desenvolvido através de uma Iniciação Científica financiada pela Pontifícia Universidade Católica de Campinas (PUC-Campinas), tem como 
    objetivo mensurar os dispêndios públicos municipais e estaduais em Ciência e Tecnologia (C&T) no município de Campinas/SP, durante o período de 2016 a 2024.

    Para consultar os resultados, a metodologia e o material utilizado, navegue pelo menu lateral.
    '''
)

st.markdown('***')

col1, col2, col3, col4, col5 = st.columns([3, 1, 2, 1, 3])

with col3:
    st.image("arquivos/logo-pucc.png", width=200)
