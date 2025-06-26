<style>
/* Remove toda borda inferior laranja de qualquer aba do Streamlit */
div[role="tablist"] > button {
    border-bottom: 3.5px solid transparent !important;
    box-shadow: none !important;
}

/* Define borda azul para aba ativa */
div[role="tablist"] > button[aria-selected="true"] {
    border-bottom: 3.5px solid #3f5c85 !important;
    box-shadow: 0 3px 8px rgb(63 92 133 / 0.22) !important;
    color: #3f5c85 !important;
    background-color: rgba(63, 92, 133, 0.14) !important;
    font-weight: 700 !important;
}

/* Container das abas - fixar no topo */
div[role="tablist"] {
    display: flex !important;
    gap: 16px !important;
    padding: 14px 28px !important;
    background: rgba(20, 35, 55, 0.9) !important;
    border-radius: 14px 14px 0 0 !important;
    margin: 0 !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 9999 !important;
    box-shadow: 0 2px 8px rgb(0 0 0 / 0.12) !important;
    user-select: none !important;
}

/* Abas individuais */
div[role="tablist"] > button {
    background: transparent !important;
    color: #a0b8d9 !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 12px 28px !important;
    border-radius: 10px 10px 0 0 !important;
    transition: color 0.3s ease, border-bottom-color 0.3s ease, background-color 0.25s ease;
    cursor: pointer !important;
}

/* Hover abas não ativas */
div[role="tablist"] > button:not([aria-selected="true"]):hover {
    color: #5a7ca6 !important;
    background-color: rgba(90, 124, 166, 0.1) !important;
    border-bottom-color: transparent !important;
}

/* Conteúdo das abas */
.css-1d391kg > div[role="tabpanel"] {
    background-color: #f2f6fb !important;
    border-radius: 0 14px 14px 14px !important;
    padding: 30px 36px !important;
    box-shadow: 0 6px 20px rgb(63 92 133 / 0.12) !important;
    border: 1.5px solid rgba(63, 92, 133, 0.12) !important;
    margin-bottom: 48px !important;
}

/* Fonte geral */
html, body, .block-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    color: #223344 !important;
    background-color: #e8edf4 !important;
}

/* Remove barra lateral */
[data-testid="stSidebar"] {display: none !important;}

/* Remove menu superior */
header {display: none !important;}

/* Remove rodapé */
footer {display: none !important;}

/* Ajusta container principal sem padding esquerdo e superior */
.css-1d391kg {
    padding-left: 0 !important;
    padding-top: 0 !important;
}

/* Remove margem padrão da main block container */
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
</style>
