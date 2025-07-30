import streamlit as st

st.markdown('## Equipe')

st.markdown(
    """
    <style>
    a {
        text-decoration: none;
        color: #003366;  /* azul institucional, opcional */
    }
    a:hover {
        text-decoration: underline;  /* sublinha no hover, opcional */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p><strong>Orientadora:</strong> Prof.ª Dr.ª Daniela Scarpa Beneli&#8195;
    <a href="http://lattes.cnpq.br/3699082804969492" target="_blank">🔍︎ Lattes</a></p>
    <p><strong>Orientando:</strong> Breno Henrique de Oliveira&#8195;
    <a href="http://lattes.cnpq.br/1654783111555271" target="_blank">🔍︎ Lattes</a></p>
    """,
    unsafe_allow_html=True
)
