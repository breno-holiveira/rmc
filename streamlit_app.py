import streamlit as st

def navigation():
    params = st.experimental_get_query_params()
    path = params.get('p', ['home'])[0]
    return path

def nav_bar():
    current = navigation()
    pages = ["home", "results", "analysis", "examples", "logs", "verify", "config"]
    labels = {
        "home": "Home",
        "results": "Results",
        "analysis": "Analysis",
        "examples": "Examples",
        "logs": "Logs",
        "verify": "Verify",
        "config": "Config"
    }

    cols = st.columns(len(pages))
    for i, p in enumerate(pages):
        if cols[i].button(labels[p], key=p):
            st.experimental_set_query_params(p=p)

page = navigation()

nav_bar()

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
