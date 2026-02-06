import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio
from configuracoes.funcoes import (tema_plotly,abrir_arquivo)


# --- configurando o tema dos graficos. ---- 

tema_plotly()



# inportando as DF:
df = abrir_arquivo()

# --- Configurando a Pagina ---
st.set_page_config(
    page_title= "Análise do Perfil de Cancelamentos",
    page_icon= "🚖",
    layout='wide'
    
)

with st.sidebar:
    

    st.markdown(
        '''
        - Criado por : Thiago Martins
        - Linkedin : [Meu perfil](https://www.linkedin.com/in/thiagomartins1993/)
        - GitHub : [Meus Projetos](https://github.com/ThiagoMartins-Lages/Portfolio)
        '''
    )


st.markdown("# :bar_chart: Avaliação do Perfil de Cancelamentos Uber Índia")

# --- Perguntas de Negocio --- 
# avaliando taxa cancelamento. 

    # Media de cancelamento por tipo de Usuario
cancelamento_mot = df['Corridas Canceladas pelo Motorista'].mean()
cancelamento_pass = df['Corridas Canceladas pelo Cliente'].mean()
    # Motivo de canselamento por Usuario
mot_cliente =(
    df[df['Situação da Corrida'] == 'Cancelled by Customer']['Motivo do Cancelamento do Cliente'].value_counts(dropna=True)
)
mot_motorista =(
    df[df['Situação da Corrida'] == 'Cancelled by Driver']['Motivo do Cancelamento do Motorista'].value_counts(dropna=True)
)

    #Analise das Situação das corridas.
situ_corridas = df['Situação da Corrida'].value_counts(dropna=True).reset_index()

    # Gerando DataFrames para analizar receitas.
receita_cor_concluidas = df[df['Situação da Corrida'].isin(['Completed','Incomplete']) ]['Valor da Reserva'].sum()
receita_perdida = df[~df['Situação da Corrida'].isin(['Completed','Incomplete'])]['Valor da Reserva'].sum()

receita = pd.DataFrame({
    'Tipo' : ['Receita Gerada','Custo com Cancelamento','Receita Total Possivel'],
    'Valor' : [receita_cor_concluidas,receita_perdida,receita_cor_concluidas + receita_perdida]
})

receita['Monetario'] = receita['Valor'].apply(lambda x: f'₹ {x:,.2f}')
receita = receita.sort_values(by='Valor',ascending=False)


# --- Dashboard ---
with st.container(key= 'Cancelamentos'):
    st.markdown("## :taxi: Cancelamentos")
    with st.expander(label='Cancelamentos por usuário e motivos',expanded=False,icon='🚫'):
        col1,col2 = st.columns(2)

        with col1:

            # Grafico de proporção de cancelamentos por Usuario
            fig = px.pie(
                values=[cancelamento_mot,cancelamento_pass],
                names=['Motoristas','Passageiros'],
                title='Média de Cancelamento por tipo de Usuário',
                )
            fig.update_traces(
                textfont = dict(
                    size=16,
                    color="black",
                    family="Arial",
                    weight="bold"
                )
            )
            fig.update_layout(
                legend= dict(
                    yanchor='top',
                    y=1,
                    xanchor='right',
                    x=-0.1
                )

            )
            st.plotly_chart(fig,width='stretch')

            # Grafico de proporção de situação de corridas
            fig = px.pie(
                values=situ_corridas['count'],
                names=situ_corridas['Situação da Corrida'],
                title='Relação Situação das Corridas'
            )
            fig.update_traces(
                textfont = dict(
                    size=16,
                    color="black",
                    family="Arial",
                    weight="bold"
                )
            )
            fig.update_layout(
                legend= dict(
                    yanchor='top',
                    y=1,
                    xanchor='right',
                    x=-0.1
                )
            )
            st.plotly_chart(fig,width='stretch')
            with st.expander(label='Análise',expanded=False,icon='✍️'):
                st.markdown(
                    '''
                    - Pode-se verificar que, apesar de a maior parte das corridas serem completadas, há uma elevada taxa de cancelamente, principalmente quando se verifica a taxa de cancelamento pelo motorista
                    - Somando todos os cancelamentos, eles representam 32% de todas as corridas registradas.
                    '''
                )



        with col2:
            fig = px.pie(
                values=mot_cliente,
                names=mot_cliente.index,
                title='Motivo de Cancelamento do Passageiro'
            )
            fig.update_traces(
                textfont = dict(
                    size=12,
                    color="black",
                    family="Arial",
                    weight="bold"
                )
            )
            st.plotly_chart(fig,width='stretch')

            fig = px.pie(
                values=mot_motorista,
                names=mot_motorista.index,
                title='Motivo de Cancelamento do Motorista'
            )
            fig.update_traces(
                textfont = dict(
                    size=12,
                    color="black",
                    family="Arial",
                    weight="bold",
                    
                ),
            )
            
            st.plotly_chart(fig,width='stretch')

            with st.expander(label='Análise',expanded=False,icon='✍️'):
                st.markdown(
                    '''
                    Os motivos de cancelamento pelo motorista possuem valores muito semelhantes. Isso pode implicar em uma prática abusiva já analisada no Brasil,
                    em que os motoristas de aplicativo cancelam as corridas de forma abusiva e/ou estratégica, visando aumento na tarifa.

                    Os cancelamentos abusivos evidenciados no gráfico dos Motoristas, aliados ao fato de que 22,2% das ocorrências canceladas pelos clientes
                    se devem à falta de deslocamento do motorista em sua direção, indicam possível comportamento inadequado por parte de alguns motoristas, 
                    comprometendo diretamente a experiência do usuário na plataforma.

                    - Estes comportamentos precisam ser tratados na região. 
                    - Um exemplo de como coibir essa atitude pode ser o método utilizado pela UBER Brasil, que, ao observar o comportamento dos motoristas, realiza o banimento da plataforma caso as atitudes sejam consideradas abusivas e recorrentes.

                        - [Fonte 1 - Catraca Livre](https://catracalivre.com.br/variedades/motoristas-da-uber-podem-ser-expulsos-da-plataforma-por-causa-disso)

                        - [Fonte 2 - Diário do Comércio](https://diariodocomercio.com.br/mix/motoristas-da-uber-sao-avisados-sobre-possivel-exclusao-da-plataforma)

                    ''',width="content"
                )


    with st.expander(label='Perdas pelos Cancelamentos',expanded=False,icon='💰'):
        col_esq,col_dir = st.columns(2)
        with col_esq:
            fig = px.bar(
                receita,x='Tipo',y='Valor',
                hover_data='Valor',
                color='Valor',
                text='Monetario',
                title='Perdas de Receita por Cancelamento'
            )
            fig.update_traces(
                textfont= dict(
                    weight='bold'
                )
            )
            fig.update_yaxes(visible=False)
            fig.update_coloraxes(
                showscale=False
            )
            st.plotly_chart(fig,width='stretch')
        with col_dir:
            fig = px.pie(
                values=[receita_cor_concluidas,receita_perdida],
                names=['Receita Gerada','Custo com Cancelamento'],
                title='Proporção de perdas com cancelamentos',
                labels=['Receita Gerada','Custo com Cancelamento']
            )
            fig.update_traces(
                textfont= dict(
                    size=16,
                    color='black',
                    family='Arial',
                    weight="bold"
                )
            )
            st.plotly_chart(fig,width='stretch')
        with st.expander(label='Análise',expanded=False,icon='✍️'):
            st.markdown(
                '''
                - Notas do Gráfico.
                    - A Receita Gerada é o total gerado no somatório entre as corridas completadas e as corridas interrompidas
                    - As corridas interrompidas foram consideradas neste cálculo, pois mesmo interrompidas, há um valor a ser pago pela distância percorrida
                    - O Custo com Cancelamento é o valor que foi deixado de ser gerado considerando todas as corridas canceladas e com motoristas não encontrados
                    - A Receita Total Possivel é o somatório **Receita Gerada** e **Custo com Cancelamento**, representando o valor total que poderia ser gerado caso não houvesse cancelamentos
                    - Observando o **Custo com o Cancelamento**, podemos verificar que ele representa **27%** da Receita Total Possivel.
                '''
            )
            st.markdown(
                '''
                #### Conclusão
                <p>Os cancelamentos de corridas na região analisada estão gerando uma perda estimada de <b>27%</b> na receita operacional local. A elevada taxa de cancelamentos,
                atribuída a possíveis práticas abusivas por parte de determinados motoristas da comunidade, demanda uma intervenção corretiva imediata.</p>
                <p>Conforme apontado na análise de <i>Perfil de Cancelamentos</i>, <b>72%</b> de todas as corridas canceladas foram pelos próprios motoristas, 
                sugerindo um padrão sistemático que pode configurar um comportamento oportunista. Este cenário está associado a um impacto financeiro direto de aproximadamente <b>₹ 14.307.840,00</b> ,
                equivalente a <b>R$ 850.470,40</b> , representando um risco significativo à sustentabilidade da operação na região.</p>
                ''',width='content',unsafe_allow_html=True
            )