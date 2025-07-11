import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Importação das páginas
from paginas import despesas, receitas, pib, emprego, homicidios, transito, sobre, inicio

# INICIALIZAÇÃO DASH
app = dash.Dash(__name__, external_stylesheets=["assets/style.css"])
app.title = "RMC em Números"

# LAYOUT PRINCIPAL
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # <-- Monitorar URL

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
                    html.Li([html.A("Início", href="/", className="nav-link-bottom")], className="nav-item-bottom"),

                    html.Li([html.A("Sobre", href="/sobre", className="nav-link-bottom")], className="nav-item-bottom"),

                    html.Li([
                        html.A("Economia", href="#", className="nav-link-bottom dropdown-toggle", id="economia-dropdown"),
                        html.Ul([
                            html.Li([html.A("Produto Interno Bruto", href="/economia/pib", className="dropdown-link")]),
                            html.Li([html.A("Emprego", href="/economia/emprego", className="dropdown-link")])
                        ], className="dropdown-menu", id="economia-menu")
                    ], className="nav-item-bottom dropdown"),

                    html.Li([
                        html.A("Finanças", href="#", className="nav-link-bottom dropdown-toggle", id="financas-dropdown"),
                        html.Ul([
                            html.Li([html.A("Despesas", href="/financas/despesas", className="dropdown-link")]),
                            html.Li([html.A("Receitas", href="/financas/receitas", className="dropdown-link")])
                        ], className="dropdown-menu", id="financas-menu")
                    ], className="nav-item-bottom dropdown"),

                    html.Li([
                        html.A("Segurança", href="#", className="nav-link-bottom dropdown-toggle", id="seguranca-dropdown"),
                        html.Ul([
                            html.Li([html.A("Taxa de homicídios", href="/seguranca/homicidios", className="dropdown-link")]),
                            html.Li([html.A("Acidentes de Trânsito", href="/seguranca/transito", className="dropdown-link")])
                        ], className="dropdown-menu", id="seguranca-menu")
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

# =====================
# CALLBACKS
# =====================

# 🟡 Callback da Busca
@app.callback(
    Output("page-content", "children"),
    [Input("search-button", "n_clicks")],
    [State("search-input", "value")]
)
def search_content(n_clicks, search_value):
    if n_clicks > 0 and search_value:
        return html.Div([
            html.H3(f"Resultados da busca para: '{search_value}'"),
            html.P("Funcionalidade de busca preparada para conteúdo em /paginas")
        ])
    return html.Div()

# 🔵 Callback de navegação por URL
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page(pathname):
    if pathname == "/" or pathname == "/inicio":
        return inicio.layout
    elif pathname == "/sobre":
        return sobre.layout
    elif pathname == "/economia/pib":
        return pib.layout
    elif pathname == "/economia/emprego":
        return emprego.layout
    elif pathname == "/financas/despesas":
        return despesas.layout
    elif pathname == "/financas/receitas":
        return receitas.layout
    elif pathname == "/seguranca/homicidios":
        return homicidios.layout
    elif pathname == "/seguranca/transito":
        return transito.layout
    else:
        return html.Div([
            html.H2("Página não encontrada"),
            html.P(f"URL: {pathname}")
        ])

# 🟣 Callbacks para abrir/fechar os menus dropdown (Economia, Finanças, Segurança)
@app.callback(
    Output("economia-menu", "style"),
    Input("economia-dropdown", "n_clicks"),
    prevent_initial_call=True
)
def toggle_menu_economia(n):
    return {"display": "block" if n and n % 2 == 1 else "none"}

@app.callback(
    Output("financas-menu", "style"),
    Input("financas-dropdown", "n_clicks"),
    prevent_initial_call=True
)
def toggle_menu_financas(n):
    return {"display": "block" if n and n % 2 == 1 else "none"}

@app.callback(
    Output("seguranca-menu", "style"),
    Input("seguranca-dropdown", "n_clicks"),
    prevent_initial_call=True
)
def toggle_menu_seguranca(n):
    return {"display": "block" if n and n % 2 == 1 else "none"}

# =====================
# INICIAR SERVIDOR
# =====================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
