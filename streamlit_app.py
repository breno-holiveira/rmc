import streamlit as st

st.set_page_config(
    page_title='RMC Data',
    initial_sidebar_state='collapsed',
    layout='wide'
)

# HTML e CSS da navbar
nav_html = """
<style>
    .navbar {
        background-color: #0B1D3A;
        padding: 0 2rem;
        height: 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: Arial, sans-serif;
    }
    .navbar-title {
        color: white;
        font-size: 22px;
        font-weight: bold;
        margin-right: 30px;
    }
    .nav-links {
        display: flex;
        gap: 0;
        height: 100%;
    }
    .nav-item {
        position: relative;
        height: 100%;
    }
    .nav-link {
        color: #E0E6F0;
        text-decoration: none;
        padding: 0 20px;
        height: 100%;
        display: flex;
        align-items: center;
        font-size: 14px;
        transition: all 0.1s ease;
    }
    .nav-link:hover {
        color: white;
        background-color: #1F355A;
    }
    .dropdown-content {
        position: absolute;
        top: 100%;
        left: 0;
        background-color: #0B1D3A;
        min-width: 180px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
        display: none;
        border-top: 2px solid #2D4375;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    .dropdown-item {
        color: #E0E6F0;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        font-size: 13px;
        transition: all 0.1s ease;
        border-left: 3px solid transparent;
    }
    .dropdown-item:hover {
        background-color: #1F355A;
        border-left: 3px solid #4F46E5;
    }
</style>

<div class="navbar">
    <div class="navbar-title">RMC Data</div>
    <div class="nav-links">
        <div class="nav-item">
            <a href="#" class="nav-link">Home</a>
        </div>
        <div class="nav-item dropdown">
            <a href="#" class="nav-link">About</a>
            <div class="dropdown-content">
                <a href="#" class="dropdown-item">Our Team</a>
                <a href="#" class="dropdown-item">Mission</a>
                <a href="#" class="dropdown-item">History</a>
            </div>
        </div>
        <div class="nav-item">
            <a href="#" class="nav-link">Economy</a>
        </div>
        <div class="nav-item">
            <a href="#" class="nav-link">Finance</a>
        </div>
        <div class="nav-item">
            <a href="#" class="nav-link">Security</a>
        </div>
        <div class="nav-item">
            <a href="https://github.com/breno-holiveira/rmc" target="_blank" class="nav-link">GitHub</a>
        </div>
    </div>
</div>
"""

# Renderizar a navbar
st.markdown(nav_html, unsafe_allow_html=True)

# Espaço após navbar
st.markdown("<br><br><br>", unsafe_allow_html=True)

# Conteúdo principal
st.title("Sistema RMC Data")
st.write("Selecione uma opção no menu superior para navegar.")
