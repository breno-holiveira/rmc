import os
import streamlit as st
from streamlit_navigation_bar import st_navbar
import pages as pg

# Set page configuration
st.set_page_config(page_title='RMC Data',
                   initial_sidebar_state='collapsed',
                   page_icon='icon.svg',
                   layout='wide')

# Define pages and their corresponding functions
pages = ['Início', 'Sobre', 'Economia', 'Finanças', 'Segurança', 'GitHub']
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, 'cubes.svg')
urls = {'GitHub': 'https://github.com/breno-holiveira/rmc'}

# Define styles for the navigation bar
styles = {
    "nav": {
        "background-color": "#0B1D3A",
        "justify-content": "space-between",
        "padding": "10px 20px",
        "border-radius": "5px",
    },
    "img": {
        "padding-right": "14px",
        "height": "40px",  # Adjust logo height
    },
    "span": {
        "color": "#E0E6F0",
        "padding": "14px",
        "transition": "background-color 0.3s",
    },
    "active": {
        "background-color": "#1F355A",
        "color": "#FFFFFF",
        "font-weight": "bold",
        "padding": "14px",
        "border-radius": "5px",
    },
    "hover": {
        "background-color": "#1F355A",
        "color": "#FFFFFF",
    }
}

# Options for the navigation bar
options = {
    "show_menu": True,
    "show_sidebar": False,
}

# Create the navigation bar
page = st_navbar(
    pages,
    logo_path=logo_path,
    urls=urls,
    styles=styles,
    options=options,
)

# Define functions for each page
functions = {
    "Início": pg.show_home,
    "Sobre": pg.show_about,
    "Economia": pg.show_economy,
    "Finanças": pg.show_finance,
    "Segurança": pg.show_security,
    "GitHub": pg.show_github,
}

# Navigate to the selected page
go_to = functions.get(page)
if go_to:
    go_to()
