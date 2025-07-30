import streamlit as st
import re

with open("arquivos/logo-pucc.svg", "r", encoding="utf-8") as f:
    svg_raw = f.read()

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

match = re.search(r"<svg.*?</svg>", svg_raw, re.DOTALL)
svg_clean = match.group(0) if match else svg_raw  # Fallback se regex falhar

# Exibe o SVG centralizado
st.markdown(
    f"""
    <div style="text-align: center;">
        {svg_clean}
    </div>
    """,
    unsafe_allow_html=True
)
