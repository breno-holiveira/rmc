import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Inicializar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP
])

# Configurar o título da página
app.title = "RMC Data"

# Servir arquivos estáticos
app.css.config.serve_locally = True

# Layout principal da aplicação
app.layout = html.Div([
    # Incluir CSS personalizado
    html.Link(
        rel='stylesheet',
        href='/assets/style.css'
    ),
    # Navbar superior - Primeira linha
    html.Nav([
        html.Div([
            # Logo/Nome do site à esquerda
            html.Div([
                html.A("RMC Data", href="/", className="navbar-brand")
            ], className="navbar-left"),
            
            # Barra de pesquisa e botão à direita
            html.Div([
                html.Div([
                    dcc.Input(
                        id="search-input",
                        type="text",
                        placeholder="Search",
                        className="search-input"
                    ),
                    html.Button(
                        "Search",
                        id="search-button",
                        className="search-button",
                        n_clicks=0
                    )
                ], className="search-container")
            ], className="navbar-right")
        ], className="navbar-top-content")
    ], className="navbar-top"),
    
    # Navbar inferior - Segunda linha
    html.Nav([
        html.Div([
            # Links de navegação
            html.Ul([
                html.Li([
                    html.A("Início", href="/", className="nav-link")
                ], className="nav-item"),
                
                html.Li([
                    html.A("Sobre", href="/sobre", className="nav-link")
                ], className="nav-item"),
                
                # Link com dropdown
                html.Li([
                    html.Div([
                        html.A("Economia", href="/economia", className="nav-link dropdown-toggle"),
                        html.Div([
                            html.A("Subitem 1", href="/economia/subitem1", className="dropdown-item"),
                            html.A("Subitem 2", href="/economia/subitem2", className="dropdown-item")
                        ], className="dropdown-menu")
                    ], className="dropdown")
                ], className="nav-item"),
                
                html.Li([
                    html.A("Finanças", href="/financas", className="nav-link")
                ], className="nav-item")
            ], className="nav-list")
        ], className="navbar-bottom-content")
    ], className="navbar-bottom"),
    
    # Conteúdo principal (vazio por enquanto)
    html.Main([
        html.Div([
            # Conteúdo será adicionado posteriormente em /paginas
        ], className="main-content")
    ], className="main-container")
])

# Callback para funcionalidade da barra de busca
@callback(
    Output('search-input', 'value'),
    Input('search-button', 'n_clicks'),
    prevent_initial_call=True
)
def handle_search(n_clicks):
    """
    Callback para lidar com a funcionalidade de busca.
    Por enquanto, apenas limpa o campo de busca.
    A funcionalidade real será implementada quando as páginas forem criadas.
    """
    if n_clicks > 0:
        # Aqui será implementada a lógica de busca real
        # Por enquanto, apenas retorna uma string vazia para limpar o campo
        return ""
    return dash.no_update

# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8051)

