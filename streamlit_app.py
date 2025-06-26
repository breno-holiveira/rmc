import streamlit as st

def navigation():
    params = st.query_params
    path = params.get('p', ['home'])[0]
    return path

# Barra de navegação (menu simples)
def nav_bar():
    st.markdown(
        """
        <style>
        .nav {
            display: flex;
            gap: 15px;
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .nav a {
            text-decoration: none;
            color: #0366d6;
            font-weight: 600;
            font-size: 16px;
        }
        .nav a.selected {
            color: #000000;
            font-weight: 700;
            border-bottom: 2px solid #0366d6;
        }
        </style>
        """, unsafe_allow_html=True
    )

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

    nav_html = '<nav class="nav">'
    for p in pages:
        cls = "selected" if p == current else ""
        nav_html += f'<a href="?p={p}" class="{cls}">{labels[p]}</a>'
    nav_html += '</nav>'

    st.markdown(nav_html, unsafe_allow_html=True)


page = navigation()

# Exibe barra de navegação no topo
nav_bar()

# Conteúdo das páginas
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
