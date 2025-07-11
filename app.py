"""
RMC Data - Site acadêmico minimalista com Dash
Inspirado no Harvard Dataverse Support
"""

import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Inicialização da aplicação Dash
app = dash.Dash(__name__, external_stylesheets=["assets/style.css"])
app.title = "RMC Data"

# Layout principal da aplicação
app.layout = html.Div([
    # Primeira linha da navbar: Logo e busca
    html.Div([
        html.Div([
            # Logo/Nome do site - estilo Harvard
            html.Div([
                html.A("RMC Data", href="/", className="navbar-brand")
            ], className="navbar-logo-top"),
            
            # Barra de busca e Contact Us
            html.Div([
                dcc.Input(
                    id="search-input",
                    type="text",
                    placeholder="",
                    className="search-input-top"
                ),
                html.Button(
                    "Search",
                    id="search-button",
                    className="search-button-top",
                    n_clicks=0
                ),
                html.A("Contact Us", href="/contact", className="contact-link-top")
            ], className="top-search-contact-area")
        ], className="navbar-top-container")
    ], className="navbar-top"),
    
    # Segunda linha da navbar: Links de navegação
    html.Div([
        html.Div([
            html.Nav([
                html.Ul([
                    html.Li([
                        html.A("Início", href="/", className="nav-link-bottom")
                    ], className="nav-item-bottom"),
                    
                    html.Li([
                        html.A("Sobre", href="/sobre", className="nav-link-bottom")
                    ], className="nav-item-bottom"),
                    
                    html.Li([
                        html.A("Economia", href="/economia", className="nav-link-bottom dropdown-toggle", id="economia-dropdown"),
                        html.Ul([
                            html.Li([html.A("Subitem 1", href="/economia/subitem1", className="dropdown-link")]),
                            html.Li([html.A("Subitem 2", href="/economia/subitem2", className="dropdown-link")])
                        ], className="dropdown-menu", id="economia-menu")
                    ], className="nav-item-bottom dropdown"),
                    
                    html.Li([
                        html.A("Finanças", href="/financas", className="nav-link-bottom")
                    ], className="nav-item-bottom")
                ], className="nav-menu-bottom")
            ], className="navbar-bottom-nav")
        ], className="navbar-bottom-container")
    ], className="navbar-bottom"),
    
    # Área de conteúdo principal (vazia conforme solicitado)
    html.Main([
        html.Div(id="page-content", className="main-content")
    ], className="main")
])

# Callback para funcionalidade de busca
@app.callback(
    Output("page-content", "children"),
    [Input("search-button", "n_clicks")],
    [State("search-input", "value")]
)
def search_content(n_clicks, search_value):
    """
    Callback para processar buscas
    Preparado para buscar em /paginas quando implementado
    """
    if n_clicks > 0 and search_value:
        return html.Div([
            html.H3(f"Resultados da busca para: \'{search_value}\'"),
            html.P("Funcionalidade de busca preparada para conteúdo em /paginas")
        ], className="search-results")
    return html.Div()

# Callback para dropdown do menu Economia
@app.callback(
    Output("economia-menu", "style"),
    [Input("economia-dropdown", "n_clicks")]
)
def toggle_dropdown(n_clicks):
    """
    Callback para mostrar/esconder dropdown do menu Economia
    """
    if n_clicks and n_clicks % 2 == 1:
        return {"display": "block"}
    return {"display": "none"}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
