import streamlit as st

def navigation():
    # Usar st.experimental_get_query_params (ou st.query_params no Streamlit >=1.21)
    # para obter o parâmetro 'p' da URL
    params = st.experimental_get_query_params()
    path = params.get('p', ['home'])[0]  # default 'home' se não houver parâmetro
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
