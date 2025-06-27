# ... (restante do código igual)
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400&display=swap" rel="stylesheet">
    <style>
        .stHorizontalBlock span {
            font-family: 'Work Sans', sans-serif !important;
            font-weight: 300 !important;
            font-size: 15px !important;
            padding: 6px 6px !important;
            margin: 0 6px !important;
            color: rgba(255,255,255,0.80) !important;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
            position: relative;
            transition: color 0.25s ease;
        }
        .stHorizontalBlock span:hover {
            color: #ff9e3b !important;
        }
        .stHorizontalBlock [aria-selected="true"] span {
            font-weight: 300 !important;
            color: #e3a86a !important; /* tom suave, sem brilho */
        }
        .stHorizontalBlock [aria-selected="true"] span::after {
            content: none !important;
        }
        .stHorizontalBlock {
            background-color: #1f2937 !important;
            padding: 0 !important;
            height: 44px !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: left !important;
            user-select: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
