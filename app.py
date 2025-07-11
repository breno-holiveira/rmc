# app.py
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import os
import markdown

# Inicializa o app com Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "RMC em Números"

# Lê o conteúdo markdown das páginas na pasta /paginas
def load_page(page):
    path = os.path.join("paginas", f"{page}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return dcc.Markdown(f.read())
    return html.Div("Página não encontrada.")

# Lista de páginas disponíveis
paginas_disponiveis = [f.split(".md")[0] for f in os.listdir("paginas") if f.endswith(".md")]

# Layout
app.layout = html.Div([
    # NAVBAR - LINHA SUPERIOR
    html.Div([
        html.Div("RMC em Números", className="titulo-navbar"),
        html.Div([
            dbc.Input(id="input-busca", placeholder="Buscar...", type="text", className="input-busca"),
            dbc.Button("Buscar", id="botao-busca", color="primary", className="botao-busca")
        ], className="container-busca")
    ], className="navbar-topo"),

    # NAVBAR - LINHA INFERIOR
    dbc.Navbar([
        dbc.Nav([
            dbc.NavLink("Início", href="/", active="exact"),
            dbc.NavLink("Sobre", href="/sobre", active="exact"),

            dbc.DropdownMenu([
                dbc.DropdownMenuItem("PIB a preços de mercado", href="/pib-precos"),
                dbc.DropdownMenuItem("PIB per capita", href="/pib-percapita"),
            ], label="Economia", nav=True, toggle_style={"cursor": "pointer"}),

            dbc.DropdownMenu([
                dbc.DropdownMenuItem("Despesas", href="/despesas"),
                dbc.DropdownMenuItem("Receitas", href="/receitas"),
            ], label="Finanças", nav=True, toggle_style={"cursor": "pointer"}),

            dbc.DropdownMenu([
                dbc.DropdownMenuItem("Taxa de homicídios", href="/homicidios"),
                dbc.DropdownMenuItem("Acidentes de trânsito", href="/transito"),
            ], label="Segurança", nav=True, toggle_style={"cursor": "pointer"}),
        ], pills=True)
    ], className="navbar-inferior"),

    # CONTEÚDO PRINCIPAL
    dcc.Location(id="url"),
    html.Div(id="pagina-conteudo", className="pagina-conteudo")
])

# Callback de navegação
@app.callback(Output("pagina-conteudo", "children"), Input("url", "pathname"))
def mostrar_pagina(pathname):
    pagina = pathname.lstrip("/") or "inicio"
    return load_page(pagina)

# Callback de busca
@app.callback(
    Output("pagina-conteudo", "children"),
    Input("botao-busca", "n_clicks"),
    State("input-busca", "value")
)
def buscar_conteudo(n, termo):
    if not termo:
        return html.Div("Digite algo para buscar.")
    resultados = []
    for pagina in paginas_disponiveis:
        path = os.path.join("paginas", f"{pagina}.md")
        with open(path, "r", encoding="utf-8") as f:
            texto = f.read()
            if termo.lower() in texto.lower():
                resultados.append(html.Div([
                    html.H5(pagina.replace("-", " ").title()),
                    html.P(texto[:150] + "..."),
                    html.Hr()
                ]))
    if resultados:
        return resultados
    return html.Div("Nenhum resultado encontrado.")

if __name__ == "__main__":
    app.run_server(debug=True)
