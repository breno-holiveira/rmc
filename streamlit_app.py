import streamlit as st

# Configurações básicas da página
st.set_page_config(
    page_title="RMC - Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Defina as páginas disponíveis no app: chave interna e rótulo exibido
PAGES = {
    "home": "Página Inicial",
    "economia": "Economia",
    "seguranca": "Segurança",
    "financas": "Finanças Públicas"
}

def render_navbar(selected_page: str):
    """Renderiza a barra de navegação horizontal no topo"""
    cols = st.columns(len(PAGES), gap="small")
    for i, (page_key, page_label) in enumerate(PAGES.items()):
        is_selected = (page_key == selected_page)
        style = (
            """
            padding: 10px 20px;
            border-radius: 8px;
            text-align: center;
            font-weight: 600;
            user-select: none;
            cursor: default;
            """
            if is_selected else
            """
            padding: 10px 20px;
            border-radius: 8px;
            text-align: center;
            color: #4d648d;
            background-color: transparent;
            cursor: pointer;
            border: 2px solid transparent;
            transition: all 0.2s ease;
            """
        )
        hover_style = (
            "" if is_selected else "color: white; background-color: #4d648d; border-color: #4d648d;"
        )

        # Renderiza como um botão estilizado
        # Se selecionado, apenas texto; se não, botão que atualiza URL
        if is_selected:
            cols[i].markdown(
                f'<div style="background-color:#4d648d; color:white; {style}">{page_label}</div>',
                unsafe_allow_html=True
            )
        else:
            # Botão com ação para trocar página atual
            if cols[i].button(page_label):
                st.experimental_set_query_params(page=page_key)
            else:
                # Apenas para aplicar estilo hover
                cols[i].markdown(
                    f'''
                    <style>
                    div[role="button"]:hover {{
                        {hover_style}
                    }}
                    </style>
                    ''', unsafe_allow_html=True
                )

def render_home():
    st.header("Página Inicial")
    st.write("Bem-vindo ao dashboard da Região Metropolitana de Campinas.")

def render_economia():
    st.header("Economia")
    st.write("Aqui você pode colocar gráficos, análises e indicadores econômicos.")

def render_seguranca():
    st.header("Segurança")
    st.write("Informações sobre segurança pública e estatísticas criminais.")

def render_financas():
    st.header("Finanças Públicas")
    st.write("Dados sobre receitas, despesas e orçamentos públicos.")

def main():
    # Pega a página atual da URL (default "home")
    params = st.experimental_get_query_params()
    current_page = params.get("page", ["home"])[0]
    if current_page not in PAGES:
        current_page = "home"

    # Renderiza barra de navegação horizontal
    render_navbar(current_page)

    st.markdown("---")  # linha horizontal para separar navbar do conteúdo

    # Renderiza o conteúdo conforme a página selecionada
    if current_page == "home":
        render_home()
    elif current_page == "economia":
        render_economia()
    elif current_page == "seguranca":
        render_seguranca()
    elif current_page == "financas":
        render_financas()

if __name__ == "__main__":
    main()
