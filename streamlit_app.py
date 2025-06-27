import os
import streamlit as st
from streamlit_navigation_bar import st_navbar

# Set page configuration
st.set_page_config(
    page_title='RMC Data',
    initial_sidebar_state='collapsed',
    page_icon='icon.svg',
    layout='wide'
)

# Import pages module
import pages as pg

# Navigation bar configuration
pages = ['Home', 'About', 'Economy', 'Finance', 'Security', 'GitHub']
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, 'cubes.svg')
urls = {'GitHub': 'https://github.com/breno-holiveira/rmc'}

# Styling for the navigation bar
styles = {
    "nav": {
        "background-color": "#0B1D3A",
        "justify-content": "space-between",
        "padding": "0.5rem 2rem",
        "box-shadow": "0 2px 10px rgba(0,0,0,0.1)"
    },
    "img": {
        "padding-right": "14px",
        "height": "40px",
        "filter": "brightness(0) invert(1)"
    },
    "span": {
        "color": "#E0E6F0",
        "padding": "14px",
        "font-size": "1rem",
        "font-family": "sans-serif",
        "transition": "all 0.3s ease"
    },
    "active": {
        "background-color": "#1F355A",
        "color": "#FFFFFF",
        "font-weight": "600",
        "border-radius": "4px"
    }
}

# Navigation options
options = {
    "show_menu": True,
    "show_sidebar": False,
    "use_padding": False
}

# Create navigation bar
selected_page = st_navbar(
    pages,
    logo_path=logo_path,
    urls=urls,
    styles=styles,
    options=options
)

# Page routing
page_functions = {
    "Home": pg.show_home,
    "About": pg.show_about,
    "Economy": pg.show_economy,
    "Finance": pg.show_finance,
    "Security": pg.show_security,
    "GitHub": pg.redirect_to_github
}

page_function = page_functions.get(selected_page)
if page_function:
    page_function()
