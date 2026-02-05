import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏡",
    layout="centered"
)

with st.sidebar:
    

    st.markdown(
        '''
        - Criado por : Thiago Martins
        - Linkedin : [Meu perfil](https://www.linkedin.com/in/thiagomartins1993/)
        - GitHub : [Meus Projetos](https://github.com/ThiagoMartins-Lages/Portfolio)
        '''
    )

with st.container(border=True):
    st.markdown(
        '''
        # Analise de corridas Uber India

        O projeto consiste no carregamento, manipulação e analise dos dados da Base Sintetica: Uber Data Analytics Dashboard.

        - A base esta alocada no seguinte endereço -> [Kaggle](https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard)
        ''',width='content'
    )
    st.markdown(
        '''
        ---
        '''
    )

    st.markdown(
        '''
        # O Projeto

        Este projeto foi desenvolvido com o intuido de demonstrar e aprimorar habilidades praticas do dia a dia de Analise de Dados.  

        As ferramentas utilizadas nestes projeto foram:

        |Biblioteca|Uso|
        |---------|----|
        |Pandas| Limpeza e padronização dos dados, corrigindo tipos, removendo inconcistencias e tratamento de valores ausentes. Utilização para manipulação e estruturação do DataSete e geração de **Insights** alem de análise exploratoria completa.|
        |Numpy| Integração com Pandas, Matplotlib para criar piplines análiticos mais eficientes.
        |Matplotlib| Integração ao fluxo de análise do Pandas permitindo gerar graficos a partir dos DataFrames e facilitar a visualização dos dados manipulados durante a **EDA**.|
        |Seaborn| Integração ao fluxo de EDA para visualizações produzindo graficos mais limpos e vizuais mais atraentes.
        |Streamlit| Desenvolvimento de visualizações dinamicas e interativas transformando o EDA realizado em Notbooks para Dashboards multipaginas e interativas, auxiliando na visualização de **Insights**
        |Plotly| Integrado com o Streamlit para geração das visualizão utilizadas nas Dashboars. 
        '''
    )