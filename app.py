import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# INICIALIZAÇÃO DASH
app = dash.Dash(__name__, external_stylesheets=["assets/style.css"])
app.title = "RMC em Números"

# LAYOUT PRINCIPAL
app.layout = html.Div([
    # 1ª LINHA DA NAVBAR
    html.Div([
        html.Div([
            # LOGO
            html.Div([
                html.A("RMC em Números", href="/", className="navbar-brand")
            ], className="navbar-logo-top"),
            
            # BUSCA E CONTATO
            html.Div([
                dcc.Input(
                    id="search-input",
                    type="text",
                    placeholder="Digite...",
                    className="search-input-top"
                ),
                html.Button(
                    "Buscar",
                    id="search-button",
                    className="search-button-top",
                    n_clicks=0
                ),
                html.A("Contato", href="/contact", className="contact-link-top")
            ], className="top-search-contact-area")
        ], className="navbar-top-container")
    ], className="navbar-top"),
    
    # 2ª LINHA DA NAVBAR
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
                            html.Li([html.A("Produto Interno Bruto", href="/economia/pib", className="dropdown-link")]),
                            html.Li([html.A("Emprego", href="/economia/emprego", className="dropdown-link")])
                        ], className="dropdown-menu", id="economia-menu")
                    ], className="nav-item-bottom dropdown"),
                    
                    html.Li([
                        html.A("Finanças", href="/financas", className="nav-link-bottom dropdown-toggle", id="financas-dropdown"),
                        html.Ul([
                            html.Li([html.A("Despesas", href="/financas/despesas", className="dropdown-link")]),
                            html.Li([html.A("Receitas", href="/financas/receitas", className="dropdown-link")])
                        ], className="dropdown-menu", id="financas-menu")
                    ], className="nav-item-bottom dropdown"),
                ], className="nav-menu-bottom")
            ], className="navbar-bottom-nav")
        ], className="navbar-bottom-container")
    ], className="navbar-bottom"),
    
    # CONTEÚDO PRINCIPAL
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
