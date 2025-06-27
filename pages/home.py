import streamlit as st

def show_home():
    st.markdown('# RMC Data')
    
    st.markdown("""
    Apesar dos avanços na disponibilização de dados públicos nos últimos anos, o acesso a informações de qualidade em nível regional
    e municipal ainda é limitado. O **RMC Data** foi criado com o propósito de reunir, produzir e divulgar indicadores econômicos e sociais
    dos municípios da Região Metropolitana de Campinas (RMC), com foco na confiabilidade e qualidade das informações.
    
    O site foi desenvolvido por **Breno Oliveira** e **Bianca Lopes**, utilizando Python e a biblioteca Streamlit. Em caso de dúvidas ou sugestões, entre em contato por meio da aba **Contatos**.
    
    Todo o conteúdo deste site pode ser reproduzido parcial ou integralmente, sem necessidade de autorização prévia. Os dados utilizados estão disponíveis para consulta e clonagem na aba **GitHub**.
    """)
    
    st.markdown('# Região Metropolitana de Campinas')
    
    st.markdown(
        """
        A Região Metropolitana de Campinas (RMC) foi criada em 2000 pela Lei Complementar nº 870, do Estado de São Paulo, 
        e é composta por 20 municípios. 
        
        Entre seus principais destaques:
        
        - Campinas é reconhecida como a capital nacional da ciência, tecnologia e inovação.
        - É a única metrópole do interior do Brasil que não é capital estadual.
        - Considerada a melhor cidade do interior para investimentos.
        - Valinhos é classificada como a cidade mais segura do Brasil.
        """
    )
