import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import os
import markdown

# Inicializar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "RMC em Números"

# Configuração do servidor
server = app.server

# Função para ler arquivos markdown
def read_markdown_file(filename):
    """Lê um arquivo markdown e retorna o conteúdo em HTML"""
    try:
        filepath = os.path.join('paginas', filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            return markdown.markdown(content)
    except FileNotFoundError:
        return f"<h1>Página não encontrada</h1><p>O arquivo {filename} não foi encontrado.</p>"

# Função para buscar em arquivos
def search_in_files(query):
    """Busca por um termo em todos os arquivos da pasta paginas"""
    results = []
    if not query:
        return results
    
    query = query.lower()
    paginas_dir = 'paginas'
    
    if os.path.exists(paginas_dir):
        for filename in os.listdir(paginas_dir):
            if filename.endswith('.md'):
                filepath = os.path.join(paginas_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                        if query in content.lower():
                            # Extrair título (primeira linha que começa com #)
                            lines = content.split('\n')
                            title = filename.replace('.md', '').replace('_', ' ').title()
                            for line in lines:
                                if line.startswith('#'):
                                    title = line.replace('#', '').strip()
                                    break
                            
                            # Extrair snippet do conteúdo
                            content_lower = content.lower()
                            query_index = content_lower.find(query)
                            start = max(0, query_index - 50)
                            end = min(len(content), query_index + 100)
                            snippet = content[start:end]
                            
                            results.append({
                                'title': title,
                                'filename': filename,
                                'snippet': snippet
                            })
                except Exception as e:
                    continue
    
    return results

# Layout da navbar superior
navbar_top = html.Div([
    html.Div([
        html.Div("RMC em Números", className="navbar-title"),
        html.Div([
            dcc.Input(
                id="search-input",
                type="text",
                placeholder="Pesquisar...",
                className="search-input"
            ),
            html.Button("Buscar", id="search-button", className="search-button"),
            html.A("contatos", href="#", className="contact-link")
        ], className="navbar-right")
    ], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'})
], className="navbar-top")

# Layout da navbar inferior
navbar_bottom = html.Div([
    html.Div([
        html.Button("Início", id="btn-inicio", className="nav-button", n_clicks=0),
        html.Button("Sobre", id="btn-sobre", className="nav-button", n_clicks=0),
        
        # Dropdown Economia
        html.Div([
            html.Button("Economia ▼", id="btn-economia", className="nav-button", n_clicks=0),
            html.Div([
                html.Div("PIB a preços de mercado", id="btn-pib-mercado", className="dropdown-item", n_clicks=0),
                html.Div("PIB per capita", id="btn-pib-capita", className="dropdown-item", n_clicks=0),
            ], id="dropdown-economia", className="dropdown-content")
        ], className="dropdown"),
        
        # Dropdown Finanças
        html.Div([
            html.Button("Finanças ▼", id="btn-financas", className="nav-button", n_clicks=0),
            html.Div([
                html.Div("Despesas", id="btn-despesas", className="dropdown-item", n_clicks=0),
                html.Div("Receitas", id="btn-receitas", className="dropdown-item", n_clicks=0),
            ], id="dropdown-financas", className="dropdown-content")
        ], className="dropdown"),
        
        # Dropdown Segurança
        html.Div([
            html.Button("Segurança ▼", id="btn-seguranca", className="nav-button", n_clicks=0),
            html.Div([
                html.Div("Taxa de homicídios", id="btn-homicidios", className="dropdown-item", n_clicks=0),
                html.Div("Acidentes de trânsito", id="btn-acidentes", className="dropdown-item", n_clicks=0),
            ], id="dropdown-seguranca", className="dropdown-content")
        ], className="dropdown"),
        
    ], className="nav-menu")
], className="navbar-bottom")

# Layout principal
app.layout = html.Div([
    navbar_top,
    navbar_bottom,
    
    # Área de conteúdo
    html.Div([
        html.Div(id="page-content", className="content-area"),
        html.Div(id="search-results", className="search-results")
    ], className="main-container"),
    
    # Store para controlar dropdowns
    dcc.Store(id="dropdown-states", data={
        "economia": False,
        "financas": False,
        "seguranca": False
    })
])

# Callback para controlar dropdowns
@app.callback(
    [Output("dropdown-economia", "className"),
     Output("dropdown-financas", "className"),
     Output("dropdown-seguranca", "className"),
     Output("dropdown-states", "data")],
    [Input("btn-economia", "n_clicks"),
     Input("btn-financas", "n_clicks"),
     Input("btn-seguranca", "n_clicks")],
    [State("dropdown-states", "data")]
)
def toggle_dropdowns(economia_clicks, financas_clicks, seguranca_clicks, current_states):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return "dropdown-content", "dropdown-content", "dropdown-content", current_states
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Reset all dropdowns
    new_states = {"economia": False, "financas": False, "seguranca": False}
    
    # Toggle the clicked dropdown
    if button_id == "btn-economia":
        new_states["economia"] = not current_states["economia"]
    elif button_id == "btn-financas":
        new_states["financas"] = not current_states["financas"]
    elif button_id == "btn-seguranca":
        new_states["seguranca"] = not current_states["seguranca"]
    
    # Return classes based on states
    economia_class = "dropdown-content show" if new_states["economia"] else "dropdown-content"
    financas_class = "dropdown-content show" if new_states["financas"] else "dropdown-content"
    seguranca_class = "dropdown-content show" if new_states["seguranca"] else "dropdown-content"
    
    return economia_class, financas_class, seguranca_class, new_states

# Callback para navegação e conteúdo das páginas
@app.callback(
    Output("page-content", "children"),
    [Input("btn-inicio", "n_clicks"),
     Input("btn-sobre", "n_clicks"),
     Input("btn-pib-mercado", "n_clicks"),
     Input("btn-pib-capita", "n_clicks"),
     Input("btn-despesas", "n_clicks"),
     Input("btn-receitas", "n_clicks"),
     Input("btn-homicidios", "n_clicks"),
     Input("btn-acidentes", "n_clicks")]
)
def display_page(inicio_clicks, sobre_clicks, pib_mercado_clicks, pib_capita_clicks,
                despesas_clicks, receitas_clicks, homicidios_clicks, acidentes_clicks):
    
    ctx = dash.callback_context
    
    if not ctx.triggered:
        # Página inicial por padrão
        content = read_markdown_file('inicio.md')
        return html.Div([dcc.Markdown(content, dangerously_allow_html=True)])
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Mapear botões para arquivos
    page_mapping = {
        "btn-inicio": "inicio.md",
        "btn-sobre": "sobre.md",
        "btn-pib-mercado": "pib_precos_mercado.md",
        "btn-pib-capita": "pib_per_capita.md",
        "btn-despesas": "despesas.md",
        "btn-receitas": "receitas.md",
        "btn-homicidios": "taxa_homicidios.md",
        "btn-acidentes": "acidentes_transito.md"
    }
    
    filename = page_mapping.get(button_id, "inicio.md")
    content = read_markdown_file(filename)
    
    return html.Div([dcc.Markdown(content, dangerously_allow_html=True)])

# Callback para funcionalidade de pesquisa
@app.callback(
    [Output("search-results", "children"),
     Output("page-content", "children", allow_duplicate=True)],
    [Input("search-button", "n_clicks"),
     Input("search-input", "n_submit")],
    [State("search-input", "value")],
    prevent_initial_call=True
)
def perform_search(n_clicks, n_submit, search_query):
    if (not n_clicks and not n_submit) or not search_query:
        # Retornar página inicial se não há pesquisa
        content = read_markdown_file('inicio.md')
        return html.Div(), html.Div([dcc.Markdown(content, dangerously_allow_html=True)])
    
    results = search_in_files(search_query)
    
    if not results:
        search_content = html.Div([
            html.H3("Nenhum resultado encontrado"),
            html.P(f"Não foram encontrados resultados para '{search_query}'.")
        ])
        return search_content, html.Div()
    
    result_items = []
    for result in results:
        result_items.append(
            html.Div([
                html.Div(result['title'], className="search-result-title"),
                html.Div(f"...{result['snippet']}...", className="search-result-content"),
                html.Button(
                    "Ver página completa", 
                    id={"type": "view-page", "index": result['filename']},
                    className="search-button",
                    style={"margin-top": "10px", "font-size": "12px", "padding": "5px 10px"}
                )
            ], className="search-result-item")
        )
    
    search_content = html.Div([
        html.H3(f"Resultados da pesquisa para '{search_query}' ({len(results)} resultado{'s' if len(results) > 1 else ''})"),
        html.Div(result_items)
    ])
    
    return search_content, html.Div()

# Callback para visualizar página completa a partir dos resultados de pesquisa
@app.callback(
    Output("page-content", "children", allow_duplicate=True),
    [Input({"type": "view-page", "index": dash.dependencies.ALL}, "n_clicks")],
    prevent_initial_call=True
)
def view_page_from_search(n_clicks_list):
    ctx = dash.callback_context
    
    if not ctx.triggered or not any(n_clicks_list):
        raise dash.exceptions.PreventUpdate
    
    # Encontrar qual botão foi clicado
    button_id = ctx.triggered[0]['prop_id']
    filename = eval(button_id.split('.')[0])['index']
    
    content = read_markdown_file(filename)
    return html.Div([dcc.Markdown(content, dangerously_allow_html=True)])

# Callback para permitir pesquisa com Enter
@app.callback(
    Output("search-input", "n_submit"),
    [Input("search-input", "n_submit")],
    prevent_initial_call=True
)
def handle_enter_search(n_submit):
    return 0

# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
