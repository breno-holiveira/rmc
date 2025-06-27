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
