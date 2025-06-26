# === Estilo refinado para harmonizar com o HTML ===
st.markdown("""
<style>
/* Remove barra lateral, cabeçalho e rodapé */
[data-testid="stSidebar"], header, footer {
    display: none !important;
}
.block-container {
    padding-top: 1rem !important;
}

/* Remove linha laranja padrão das abas */
div[data-testid="stTabs"] > div > div > div > div[aria-selected="true"]::after {
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Fundo suave em tons quentes */
body, .main {
    background: linear-gradient(120deg, #fff8f9, #fceeee);
}

/* Cor das abas */
div[data-testid="stTabs"] button {
    background-color: transparent !important;
    color: #994455 !important;
    font-weight: 500;
    border-radius: 0 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    border-bottom: 3px solid #f63366 !important;
    color: #f63366 !important;
}

/* Títulos e textos */
h1, h2, h3, h4, h5, h6 {
    color: #994455 !important;
}
p, span, label, div, li {
    color: #2e2e2e;
    font-size: 15px;
}

/* DataFrame refinado */
[data-testid="stDataFrame"] {
    border: 1px solid #f2c5cb;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* Barras de gráfico */
.css-1y0tads .stPlotlyChart, .stAltairChart, .stBarChart {
    background: white !important;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* Links e interações */
a {
    color: #f63366;
}
</style>
""", unsafe_allow_html=True)
