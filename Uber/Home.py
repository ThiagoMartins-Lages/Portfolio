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
        # Análise de corridas Uber Índia

        O projeto consiste no carregamento, manipulação e análise dos dados da Base Sintética: Uber Data Analytics Dashboard.

        - A base está alocada no seguinte endereço -> [Kaggle](https://www.kaggle.com/datasets/yashdevladdha/uber-ride-analytics-dashboard)
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

        Este projeto foi desenvolvido com o intuido de demonstrar e aprimorar habilidades práticas de Análise de Dados.  

        As ferramentas utilizadas nestes projeto foram:

        |Biblioteca|Uso|
        |---------|----|
        |Pandas| Limpeza e padronização dos dados, corrigindo tipos, removendo inconcistências e tratamento de valores ausentes. Utilização para manipulação e estruturação do DataSet e geração de **Insights**, além de análise exploratória completa.|
        |Numpy| Integração com Pandas, Matplotlib para criar pipelines analíticos mais eficientes.
        |Matplotlib| Integração ao fluxo de análise do Pandas, permitindo gerar gráficos a partir dos DataFrames e facilitar a visualização dos dados manipulados durante a **EDA**.|
        |Seaborn| Integração ao fluxo de EDA para visualizações, produzindo gráficos mais limpos e visuais mais atraentes.
        |Streamlit| Desenvolvimento de visualizações dinâmicas e interativas, transformando o EDA realizado em Notbooks para Dashboards multipáginas e interativas, auxiliando na visualização de **Insights**
        |Plotly| Integrado com o Streamlit para geração das visualização utilizadas nas Dashboards. 
        '''
    )