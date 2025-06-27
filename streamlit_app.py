import streamlit as st

# Configurações da página
st.set_page_config(page_title='RMC Data', page_icon='icon.svg', layout='wide')

# Função para criar a barra de navegação
def navbar():
    st.sidebar.title("Navegação")
    pages = ['Início', 'Sobre', 'Economia', 'Finanças', 'Segurança', 'GitHub']
    selection = st.sidebar.radio("Ir para", pages)

    return selection

# Chama a função de navegação
page = navbar()

# Conteúdo das páginas
if page == 'Início':
    st.title("Bem-vindo ao RMC Data")
    st.write("Conteúdo da página Início.")
elif page == 'Sobre':
    st.title("Sobre")
    st.write("Conteúdo da página Sobre.")
elif page == 'Economia':
    st.title("Economia")
    st.write("Conteúdo da página Economia.")
elif page == 'Finanças':
    st.title("Finanças")
    st.write("Conteúdo da página Finanças.")
elif page == 'Segurança':
    st.title("Segurança")
    st.write("Conteúdo da página Segurança.")
elif page == 'GitHub':
    st.title("GitHub")
    st.write("Visite nosso repositório no GitHub.")
    st.markdown("[GitHub Repository](https://github.com/breno-holiveira/rmc)")

