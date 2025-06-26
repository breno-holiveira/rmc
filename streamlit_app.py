import streamlit as st

def navigation():
    # Obtem o parâmetro 'p' da URL usando st.query_params
    params = st.query_params
    path = params.get('p', ['home'])[0]  # padrão 'home' se não existir
    return path

page = navigation()

if page == "home":
    st.title('Home')
    st.write('This is the home page.')

elif page == "results":
    st.title('Results List')
    for item in range(25):
        st.write(f'Results {item}')

elif page == "analysis":
    st.title('Analysis')
    x, y = st.number_input('Input X'), st.number_input('Input Y')
    st.write('Result: ' + str(x + y))

elif page == "examples":
    st.title('Examples Menu')
    st.write('Select an example.')

elif page == "logs":
    st.title('View all of the logs')
    st.write('Here you may view all of the logs.')

elif page == "verify":
    st.title('Data verification is started...')
    st.write('Please stand by....')

elif page == "config":
    st.title('Configuration of the app.')
    st.write('Here you can configure the application')

else:
    st.error('Page not found.')
