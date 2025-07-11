import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import os
import markdown

# Inicializar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "RMC em Números"

# Função para ler arquivos markdown da pasta /paginas
def ler_arquivo_pagina(nome_arquivo):
    """Lê um arquivo markdown da pasta paginas e retorna o conteúdo em HTML"""
    caminho = os.path.join("paginas", f"{nome_arquivo}.md")
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            conteudo_md = arquivo.read()
            return markdown.markdown(conteudo_md)
    except FileNotFoundError:
        return f"<h1>Página não encontrada</h1><p>O arquivo {nome_arquivo}.md não foi encontrado.</p>"

# Função para buscar em todos os arquivos da pasta /paginas
def buscar_conteudo(termo_busca):
    """Busca um termo em todos os arquivos da pasta paginas"""
    resultados = []
    pasta_paginas = "paginas"
    
    if not os.path.exists(pasta_paginas):
        return []
    
    for arquivo in os.listdir(pasta_paginas):
        if arquivo.endswith(".md"):
            caminho = os.path.join(pasta_paginas, arquivo)
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = f.read().lower()
                    if termo_busca.lower() in conteudo:
                        nome_pagina = arquivo.replace(".md", "").replace("_", " ").title()
                        resultados.append({
                            "arquivo": arquivo.replace(".md", ""),
                            "nome": nome_pagina
                        })
            except:
                continue
    
    return resultados

# Navbar com duas linhas
def criar_navbar():
    """Cria a navbar com duas linhas conforme especificado"""
    
    # Primeira linha - Logo, busca e link Contatos
    primeira_linha = dbc.Row([
        dbc.Col(
            html.H4("RMC em Números", className="mb-0", style={
                     "color": "#333"}),
            width=4,
            className="d-flex align-items-center"
        ),
        dbc.Col(
            dbc.InputGroup([
                dbc.Input(
                    id="campo-busca",
                    placeholder="Pesquisar...",
                    type="text"
                ),
                dbc.Button(
                    "Buscar",
                    id="botao-busca",
                    color="primary",
                    n_clicks=0
                )
            ]),
            width=5,
            className="d-flex justify-content-end"
        ),
        dbc.Col(
            html.A("Contatos", href="#", className="nav-link-contatos", style={
                   "color": "#6c757d", "text-decoration": "none", "font-size": "0.9rem", "margin-left": "15px"}),
            width=3,
            className="d-flex align-items-center justify-content-end"
        )
    ], className="align-items-center w-100")
    
    # Segunda linha - Menu de navegação
    segunda_linha = dbc.Row([
        dbc.Col(
            dbc.Nav([
                dbc.NavItem(dbc.NavLink("Início", href="/", id="nav-inicio")),
                dbc.NavItem(dbc.NavLink("Sobre", href="/sobre", id="nav-sobre")),
                
                # Dropdown Economia
                dbc.DropdownMenu([
                    dbc.DropdownMenuItem("PIB a preços de mercado", href="/pib-precos-mercado"),
                    dbc.DropdownMenuItem("PIB per capita", href="/pib-per-capita"),
                ], label="Economia", nav=True, id="dropdown-economia"),
                
                # Dropdown Finanças
                dbc.DropdownMenu([
                    dbc.DropdownMenuItem("Despesas", href="/despesas"),
                    dbc.DropdownMenuItem("Receitas", href="/receitas"),
                ], label="Finanças", nav=True, id="dropdown-financas"),
                
                # Dropdown Segurança
                dbc.DropdownMenu([
                    dbc.DropdownMenuItem("Taxa de homicídios", href="/taxa-homicidios"),
                    dbc.DropdownMenuItem("Acidentes de trânsito", href="/acidentes-transito"),
                ], label="Segurança", nav=True, id="dropdown-seguranca"),
                
            ], pills=False, className="w-100")
        ,
            width=12
        )
    ], className="w-100")
    
    return dbc.Navbar([
        dbc.Container([
            primeira_linha,
            html.Hr(className="my-2"),  # Separador visual
            segunda_linha
        ], fluid=True)
    ], color="white", className="mb-4", style={
        "backgroundColor": "white",
        "padding-top": "10px",
        "padding-bottom": "10px"
    })

# Layout principal da aplicação
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    criar_navbar(),
    
    # Container para resultados de busca
    html.Div(id="resultados-busca", className="container mb-4"),
    
    # Container para conteúdo das páginas
    html.Div(id="conteudo-pagina", className="container")
])

# Callback para navegação entre páginas
@app.callback(
    Output("conteudo-pagina", "children"),
    Input("url", "pathname")
)
def exibir_pagina(pathname):
    """Exibe o conteúdo da página baseado na URL"""
    
    # Mapear URLs para arquivos
    mapeamento_urls = {
        "/": "inicio",
        "/sobre": "sobre",
        "/pib-precos-mercado": "pib_precos_mercado",
        "/pib-per-capita": "pib_per_capita",
        "/despesas": "despesas",
        "/receitas": "receitas",
        "/taxa-homicidios": "taxa_homicidios",
        "/acidentes-transito": "acidentes_transito"
    }
    
    # Obter nome do arquivo baseado na URL
    nome_arquivo = mapeamento_urls.get(pathname, "inicio")
    
    # Ler e retornar conteúdo
    conteudo_html = ler_arquivo_pagina(nome_arquivo)
    
    return html.Div([
        dcc.Markdown(conteudo_html, dangerously_allow_html=True)
    ])

# Callback para funcionalidade de busca
@app.callback(
    Output("url", "pathname"),
    Output("resultados-busca", "children"),
    [Input("botao-busca", "n_clicks")],
    [State("campo-busca", "value")]
)
def realizar_busca(n_clicks, termo_busca):
    """Realiza busca nos arquivos da pasta paginas e redireciona para a página do primeiro resultado"""
    
    if n_clicks == 0 or not termo_busca:
        return dash.no_update, []
    
    resultados = buscar_conteudo(termo_busca)
    
    if not resultados:
        return dash.no_update, dbc.Alert(
            f"Nenhum resultado encontrado para {termo_busca}",
            color="warning",
            className="mt-3"
        )
    
    # Redireciona para a primeira página encont    primeiro_resultado_path = f"/{resultados[0][\"arquivo\"]}".replace("_", "-")    return primeiro_resultado_path, []

# Callback para busca com Enter
@app.callback(
    Output("botao-busca", "n_clicks"),
    Input("campo-busca", "n_submit"),
    State("botao-busca", "n_clicks")
)
def busca_com_enter(n_submit, n_clicks_atual):
    """Permite busca pressionando Enter"""
    if n_submit:
        return (n_clicks_atual or 0) + 1
    return n_clicks_atual or 0

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)


