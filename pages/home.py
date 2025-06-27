import streamlit as st

def show_home():
    st.markdown('# RMC Data')
    
    st.markdown("""
    O **RMC Data** é um site de domínio público, criado com o propósito de reunir, produzir e divulgar indicadores econômicos e sociais dos municípios 
    da Região Metropolitana de Campinas (RMC), visando garantir a qualidade e a confiabilidade das informações, além de contribuir para a ampliação da 
    análise e da divulgação dos dados em nível regional e municipal.
    
    O projeto foi desenvolvido por Breno Oliveira e Bianca Lopes. Todo o conteúdo disponível pode ser reproduzido, adaptado ou redistribuído, parcial ou
    integralmente, sem necessidade de autorização prévia.
    
    Em caso de dúvidas ou sugestões, entre em contato por meio da aba Contatos.
    """)
    
    st.markdown('# Região Metropolitana de Campinas')
    
    st.markdown(
        """
    A Região Metropolitana de Campinas foi criada em 2000, por meio da Lei Complementar nº 870, do Estado de São Paulo. Composta por 20 municípios, a 
    RMC se destaca pela alta qualidade de vida e pelo constante desenvolvimento social e econômico.
    
    Entre seus principais destaques:
    - Campinas é oficialmente reconhecida como a Capital Nacional da Ciência, Tecnologia e Inovação, conforme o Projeto de Lei 3680/23.
    - A região abriga 6 municípios entre os 30 mais seguros do Brasil, com Valinhos ocupando a 1ª posição, segundo dados do IBGE e do Ministério da Saúde.
    - Campinas é a única cidade do interior do Brasil a possuir o status de metrópole, segundo o IBGE.
    - Em 2025, Campinas foi eleita a melhor cidade do interior do país para investimentos, de acordo com a *Oxford Economics Global Cities Index*.
        """
    )

# Carrega o conteúdo do HTML
with open("grafico.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Exibe o HTML
st.components.v1.html(html_content, height=800, scrolling=True)
