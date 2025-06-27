import os

import streamlit as st
from streamlit_navigation_bar import st_navbar

import pages as pg


st.set_page_config(page_title='RMC Data',
                   initial_sidebar_state='collapsed',
                   page_icon='📈',
                   layout='wide',
)

pages = ['Início', 'Sobre', 'Economia', 'Finanças', 'Segurança', 'GitHub']
parent_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(parent_dir, 'cubes.svg')
urls = {'GitHub': 'https://github.com/breno-holiveira/rmc'}
styles = {
    "nav": {
        "background-color": "#0B1D3A",
        "justify-content": "left",
    },
    "img": {
        "padding-right": "14px",
    },
    "span": {
        "color": "#E0E6F0",
        "padding": "14px",
    },
    "active": {
        "background-color": "#1F355A",
        "color": "#FFFFFF",
        "font-weight": "normal",
        "padding": "14px",
    }
}
options = {
    "show_menu": True,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    logo_path=logo_path,
    urls=urls,
    styles=styles,
    options=options,
)

functions = {
    "Home": pg.show_home,
    "Install": pg.show_install,
    "User Guide": pg.show_user_guide,
    "API": pg.show_api,
    "Examples": pg.show_examples,
    "Community": pg.show_community,
}
go_to = functions.get(page)
if go_to:
    go_to()
