st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet" />
    <style>
        /* Container navbar */
        .stHorizontalBlock {
            background-color: #1f2937 !important; /* cinza escuro */
            padding: 0 !important;
            height: 44px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
            user-select: none;
        }

        /* Itens da navbar */
        .stHorizontalBlock span {
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            font-weight: 400 !important;
            font-size: 14px !important;
            letter-spacing: 0em !important;
            padding: 6px 8px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.85) !important;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: relative;
            transition: color 0.2s ease;
            display: inline-flex !important;
            align-items: center !important;
        }

        /* Hover suave */
        .stHorizontalBlock span:hover {
            color: #9bbaff !important;  /* Azul claro, muito suave */
        }

        /* Item ativo: só muda cor da fonte para azul suave, sem efeitos */
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 600 !important;
            color: #7892c2 !important;  /* Azul pastel suave */
            background-color: transparent !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            padding-left: 8px !important;
            padding-right: 8px !important;
        }

        /* Remove underline ou ::after */
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: none !important;
        }

        /* RMC Data sempre em negrito e cor discreta */
        .stHorizontalBlock span:has-text("RMC Data") {
            font-weight: 700 !important;
            color: #8ca3cc !important; /* Azul acinzentado, discreto */
            padding-left: 10px !important;
            padding-right: 10px !important;
        }

        /* RMC Data ativo: mantém negrito, cor levemente mais escura */
        .stHorizontalBlock [aria-selected="true"] span:has-text("RMC Data") {
            color: #5a6b8c !important;
            font-weight: 700 !important;
            background-color: transparent !important;
        }

        /* Ajusta tamanho do logo SVG e margem */
        .stHorizontalBlock span:has-text("RMC Data") svg {
            height: 20px !important;
            margin-right: 6px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
