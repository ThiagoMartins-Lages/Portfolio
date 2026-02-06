# :bar_chart: Projeto Uber India
Este projeto apresenta uma analise exploratoria de dados (EDA) realizada sobre um *dataset* sintetico de corridas da Uber India. O objetivo é avaliar padrões de cancelamento, performance veicular e faturamento com sasionalidade e metodos de pagamento. 

Além da análise, foi desenvovida uma Dashboard interativa em Streamlit, permitindo visualizações de forma dinamica os principais insights obtidos. 

Para a visualização do Dashboard acesse o seguinte link -> [Streamlit](https://projetouber.streamlit.app).

Para visualização da Notbook contendo a EDA acesse o seguinte link -> [EDA](https://github.com/ThiagoMartins-Lages/Portfolio/blob/main/Uber/uber_analise.ipynb)


##  1. Extração dos Dados

O *Dataset* utilizado é sintético e foi criado com o proposito de simular de simular cenários reais de operação da Uber Inda.

## 2. Tratamento e Limpeza

Para garantir a qualidade das Análises, foi realizada um processo completo de *data cleaning* incuindo. 

### :heavy_check_mark: Tratamento de Valores Nulos.
- Imputação de valores em campos auxentes conforme contexto da varaivel

### :heavy_check_mark: Transformação de variaveis.
- Converção de coluna categoricas para tipos adequados.
- Padronização de testos e categorias.

### :heavy_check_mark: Manipulação de datas
- Conversão de strings para formato datetime.
- Extração de componentes temporais (hora, mês, dia, etc.).
- Identificação de padrões sazonais

## 3. Analise Exploratoria de Dados (EDA)
A EDA buscou responder perguntas como:
- Qual o perfil de cancelamento dos clientes e motoristas?
- Há preferencias sobre algum tipo de veiculo da plataforma?
- Qual o tipo de pagamento mais utilizado?
- Quais horários concentram maior demanda?
- Como se comporta os pedidos e o faturamento ao longo do ano ? Como é a sasionalidade?

Essas análises permitiram identificar tendências e comportamentos relevantes para tomada de decisão.

## 4. Dashboard Interativa com Streamlit
Para facilitar a visualização dos insights, foi desenvolvida uma dashboard interativa utilizando Streamlit, permitindo:
- Filtrar dados por Estatus da Corrida, tipo de Veiculo.
- Visualização Grafica Dinamica. 
- Observação de Padrões Temporais.

A aplicação oferece uma experiência intuitiva e acessível, ideal para demonstração e exploração dos resultados.

##  Tecnologias Utilizada

| Categorai | Ferramentas|
|-----------|------------|
|Linguagem| Python |
|Manipulação de Dados | Pandas, NumPy|
|Visualização| Matplotlib, Seaborn|
|Dashboard| Streamlit|