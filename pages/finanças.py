import streamlit as st

st.title("Finanças")
st.write("Nesta seção você encontrará dados financeiros.")

st.subheader("Subtópicos")
st.page_link("pages/despesas.py", label="▶️ Despesas")
st.page_link("pages/arrecadacao.py", label="▶️ Arrecadação")
