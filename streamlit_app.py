import streamlit as st

# Set page configuration
st.set_page_config(
    page_title='RMC Data',
    initial_sidebar_state='collapsed',
    page_icon='icon.svg',
    layout='wide'
)

# Custom HTML and CSS for the navigation bar
nav_html = """
<style>
    .navbar {
        display: flex;
        background-color: #0B1D3A;
        padding: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        justify-content: space-between;
        align-items: center;
    }
    .navbar img {
        height: 40px;
        filter: brightness(0) invert(1);
    }
    .navbar a {
        color: #E0E6F0;
        padding: 14px;
        text-decoration: none;
        font-size: 1rem;
        transition: background-color 0.3s;
    }
    .navbar a:hover {
        background-color: #1F355A;
        border-radius: 4px;
    }
    .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #0B1D3A;
        min-width: 160px;
        z-index: 1;
    }
    .dropdown-content a {
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
</style>

<div class="navbar">
    <img src="cubes.svg" alt="Logo">
    <div>
        <a href="#">Home</a>
        <div class="dropdown">
            <a href="#">About</a>
            <div class="dropdown-content">
                <a href="#">Team</a>
                <a href="#">Mission</a>
            </div>
        </div>
        <a href="#">Economy</a>
        <a href="#">Finance</a>
        <a href="#">Security</a>
        <a href="https://github.com/breno-holiveira/rmc" target="_blank">GitHub</a>
    </div>
</div>
"""

# Render the custom navigation bar
st.markdown(nav_html, unsafe_allow_html=True)

# Main content area
st.title("Welcome to RMC Data")
st.write("This is the main content area of your application.")
