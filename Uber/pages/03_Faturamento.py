import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from configuracoes.funcoes import (tema_plotly,abrir_arquivo,range_axis,unic_val)


# --- configurando o tema dos gráficos. ---- 

tema_plotly()




# importando as DF:
df = abrir_arquivo()

# --- Configurando a Página ---
st.set_page_config(
    page_title= "Formas de Pagamento",
    page_icon= "💳",
    layout='wide'
    
)

with st.sidebar:
    
    st.markdown('Filtros de Pagina')
    situ_corrida = st.multiselect(
        label='Selecione o Estatus de Corrida',
        options=unic_val(df,'Situação da Corrida'),
        default=[]
    )

    tipo_veiculo = st.multiselect(
        label='Selecione o Tipo de Veiculo',
        options=unic_val(df,'Tipo de Veículo'),
        default=[]
    )

    st.markdown(
        '''
        ---
        - Criado por : Thiago Martins
        - Linkedin : [Meu perfil](https://www.linkedin.com/in/thiagomartins1993/)
        - GitHub : [Meus Projetos](https://github.com/ThiagoMartins-Lages/Portfolio)
        '''
    )
if situ_corrida and not tipo_veiculo:
    df_selec = df.query(
        "`Situação da Corrida` == @situ_corrida"
    )
elif tipo_veiculo and not situ_corrida:
    df_selec = df.query(
        "`Tipo de Veículo` == @tipo_veiculo"
    )
elif situ_corrida and tipo_veiculo:
    df_selec = df.query(
        "`Situação da Corrida` == @situ_corrida & `Tipo de Veículo` == @tipo_veiculo"
    )
else:
    df_selec = df.copy()


# --- Perguntas de Negócio ---

    # Formas de pagamento mais utilizadas.
tipo_pag = df_selec.groupby('Método de Pagamento').agg({
    "ID da Reserva" : 'count',
    "Valor da Reserva" : 'sum'
})
tipo_pag = tipo_pag.reset_index()
tipo_pag['% Reservas'] = tipo_pag['ID da Reserva'] / tipo_pag['ID da Reserva'].sum()
tipo_pag['% Valor'] = tipo_pag['Valor da Reserva'] / tipo_pag['Valor da Reserva'].sum()
    # _____ 

    # Receitas por Estacão do Ano, Mês e Dia da Semana.
rec_periodica = df_selec[['ID da Reserva', 'Data','Estacao','Ano', 'Mes', 'Nome_Mes','Dia', 'Dia_Semana','DOW', 'Trimestre','Valor da Reserva']].sort_values(by='Data').copy()
rec_periodica = rec_periodica.sort_values(by='Mes')
        # receita por mês
rec_mes = rec_periodica.groupby(['Mes','Nome_Mes']).agg({
    'ID da Reserva': 'count',
    'Valor da Reserva': 'sum'
}).reset_index()


            # adicionando a variação mensal.
rec_mes['Var_abs'] = rec_mes['Valor da Reserva'].diff()
rec_mes['Var_percentual'] = rec_mes['Valor da Reserva'].pct_change()
rec_mes['cor'] = rec_mes['Var_percentual'].apply(lambda x: '#FF746C' if x < 0 else "#245A87")

        # receita por estação
rec_estacao = rec_periodica.groupby('Estacao').agg({
    'ID da Reserva': 'count',
    'Valor da Reserva': 'sum'
}).reset_index()
rec_estacao = rec_estacao.sort_values(by='Estacao')


# ______
# --- Layout ---
st.markdown("# :bar_chart: Avaliação do Faturamento gerado pela Uber India")
st.markdown(
    '''
    Breve explicação:  
    - UPI: É um método de pagamento instantâneo desenvolvido na Índia que permite transações bancárias utilizando o celular. Similar ao PIX
    '''
)

with st.expander(label='Tipos de pagamentos mais Utilizados'):
    col_esq,col_dir = st.columns(2)

    with col_esq:
        tipo_ordenado = tipo_pag.sort_values(by='% Reservas',ascending=False)
        fig = px.bar(
            data_frame=tipo_ordenado,
            x='Método de Pagamento',
            y='% Reservas',
            color='% Reservas',
            text='% Reservas',
            title='Corridas por Tipo de Pagamento'
            )
        
        fig.update_yaxes(
            title_text='% de  Reservas',
            tickformat=".0%"
            )
        
        fig.update_coloraxes(
            colorbar_title_text='% de  Reservas'
        )
        fig.update_traces(
            texttemplate="%{y:.2%}",
            textfont= dict(
                family='Arial',
                weight='bold'
            ),
            hovertemplate='% Reservas: %{y:.2%}'
        )
        st.plotly_chart(fig,width='stretch')

    with col_dir:
        tipo_ordenado = tipo_pag.sort_values(by='% Valor',ascending=False)
        fig = px.bar(
            data_frame=tipo_ordenado,
            x='Método de Pagamento',
            y='% Valor',
            color='% Valor',
            text='% Valor',
            title='Arrecadação por Tipo de Pagamento'
            )
        
        fig.update_yaxes(
            title_text='% de Arrecadação',
            tickformat=".0%"
            )
        fig.update_coloraxes(
            colorbar_title_text='% de  Arrecadação'
        )
        fig.update_traces(
            texttemplate="%{y:.2%}",
            textfont= dict(
                family='Arial',
                weight='bold'
            ),
            hovertemplate='% Valor: %{y:.2%}'
        )
        
        st.plotly_chart(fig,width='stretch')

    with st.expander(label='Analise ✍️'):
        st.markdown(
            '''
            *Notas do Gráfico*
            - Podemos verificar que **32%** das corridas não tiveram seu tipo de pagamento informado.   
            - A ausência de informações sobre o tipo de pagamento em quase um terço das corridas compromente a confiabilidade da análise de tendência.  
            
            ----
            *Motivos da Ausência de Método de Pagamento*
            - As corridas que não possuem os métodos de pagamento são justamente as com status de Canceladas e Motorista Não Encontrado.
            - A uber tem uma política de, no momento da reserva da corrida, o usuário deve informar o método de pagamento.
                - Desta forma os métodos de pagamento das corridas não estão sendo armazenados para estas ocorrências 
                - Essa falta de informação pode distorcer a conclusão sobre preferência de pagamentos dos usuários e preferências dos motoristas.
            
            ----
            *Relevância da Uber Wallet*:
            - A Uber Wallet representa apenas 8,6% dos métodos de pagamento registrados, um percentual ainda tímido diante das demais opções disponíveis.
            - A utilização da Uber Wallet também facilita a rastreabilidade de transações, tanto para o cliente quanto para o motorista, garantido mais segurança para ambos.  
            - **Transparência para motoristas**:
                - Com créditos já disponíveis na carteira digital, o motorista pode ter maior confiança na efetivação do pagamento, o que pode aumentar a taxa de aceitação de corridas.
            - **Facilidade de integração com promoções e fidelidade**:
                - A Uber pode vincular benefícios exclusivos ao uso da Wallet, como cashback, descontos ou prioridade em corridas, incentivando sua adoção.
                - Isso também pode gerar dados mais ricos sobre o comportamento do usuário, permitindo análises mais precisas e segmentadas.
            ''',width="stretch"
        )


with st.expander(label='Tendência de Faturamento ao Longo de 2024'):
    col_esq,col_dir = st.columns(2)

    with col_esq:
        # Receita e Quantidade de Reservas por Mes
        fig = go.Figure(
            go.Bar(
                x=rec_mes['Nome_Mes'],
                y=rec_mes['ID da Reserva'],
                text=rec_mes['ID da Reserva'],
                name='Qtd de Reservas',
                marker_color="#4CB5AE"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=rec_mes['Nome_Mes'],
                y=rec_mes['Valor da Reserva'],
                yaxis='y2',
                name='Receita Total',
                marker_color="#245A87",
                
            )
        )
        fig.update_layout(
            legend=dict(
                title=dict(
                    text='Legenda'
                ),
                x=0.5,
                y=1.2,
                orientation='h',
                yanchor='top',
                xanchor='center'
            ),
            yaxis=dict(
                side='left',
                title_text='Contagem de Corridas',
                range=[range_axis(rec_mes,'ID da Reserva',0.85,'min'),range_axis(rec_mes,'ID da Reserva',1.05,'max')],
                showgrid=False
            ),
            yaxis2=dict(
                side='right',
                overlaying='y',
                title_text='Faturamento',
                tickprefix='₹ ',
                tickformat='.2s',
                ticksuffix='i',
                showgrid=False,
                
            ),
            title=dict(
                text='Receita e Quantidade de Reservas por Mes'
            ),
            font=dict(
                weight=800,
            ),
            
        )

        
        st.plotly_chart(fig,width='stretch')

    with col_dir:
        # grafico de variação de valor mensal.
        fig = px.bar(
            data_frame=rec_mes,
            x='Nome_Mes',
            y='Var_percentual',
            text='Var_percentual',
            color= 'cor',
            color_discrete_map='identity',
            title='Variação de Faturamento por Mês'
        )

        fig.update_layout(
            yaxis=dict(
                title_text='Variação Mensal',
                tickformat='.2%',
                range=[range_axis(rec_mes,'Var_percentual',1.5,'min'),range_axis(rec_mes,'Var_percentual',1.5,'max')]
            ),
            xaxis=dict(
                categoryorder='array',
                categoryarray=rec_mes['Nome_Mes'],
                title='',
                

            )
        )
        
        fig.update_traces(
            texttemplate='%{y:.2%}',
            textfont=dict(
                weight='bold'
            ),
            textposition='outside'
        )

        st.plotly_chart(fig,width='stretch')
    

    # grafico faturamento por estação
    fig = go.Figure(
        go.Bar(
            x=rec_estacao['Estacao'],
            y=rec_estacao['ID da Reserva'],
            text=rec_estacao['ID da Reserva'],
            name='Qtd de Reservas',
            marker=dict(
                color=rec_estacao['ID da Reserva'],
                showscale=False
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=rec_estacao['Estacao'],
            y=rec_estacao['Valor da Reserva'],
            yaxis='y2',
            name='Receita Total',
            marker_color="#245A87"
        )
    )

    fig.update_layout(
        legend=dict(
            title=dict(
                text='Legenda'
            ),
            orientation='h',
            x=0.5,
            y=1.2,
            xanchor='center',
            yanchor='top'
        ),
        font=dict(
            weight=800,
        ),
        yaxis=dict(
            side='left',
            range=[range_axis(rec_estacao,'ID da Reserva',0.94,'min'),range_axis(rec_estacao,'ID da Reserva',1.01,'max')],
            title_text='Contagem de Corridas',
            showgrid=False
        ),
        yaxis2=dict(
            side='right',
            overlaying='y',
            title_text='Faturamento',
            showgrid=False,
            tickprefix='₹ ',
            tickformat='.2s',
            ticksuffix='i',
            range=[range_axis(rec_estacao,'Valor da Reserva',0.95,'min'),range_axis(rec_estacao,'Valor da Reserva',1.05,'max')]
        ),
        title=dict(
            text='Receita e Quantidade de Reservas por Estação do Ano'
        )
    )

    st.plotly_chart(fig,width='stretch')

    with st.expander(label='Análise ✍️'):
        st.markdown(
            '''
            **Sazonalidade**
            - Observa‑se ao longo do ano uma variação significativa no faturamento da plataforma, evidenciando forte influência sazonal sobre a demanda 
            - O mês de março apresenta o maior faturamento e também o maior crescimento positivo. Esse comportamento está associado ao **Festival Holi**,
            celebração nacional que marca a chegada da primavera.
                - Durante esse período, há um aumento expressivo na procura por hospedagens, chegando a aproximadamente cinco vezes a demanda usual, 
                conforme reportado pelo portal [Money Control](https://www.moneycontrol.com/news/technology/travel-bookings-surge-5-fold-for-holi-good-friday-holidays-temple-towns-to-see-big-rush-12464531.html)
            - A sazonalidade das corridas também é impactada pelas condições climáticas regionais.
                - O clima indiano é caracterizado por um período central do ano quente e chuvoso, influenciado pelo regime de monções, 
                o que tende a elevar a demanda por deslocamentos.
                - Na primavera, durante o auge das monções, predominam temperaturas elevadas e maior volume de chuvas.
                - No verão, as temperaturas podem ultrapassar 40°C, intensificando ainda mais a necessidade de transporte.
            ''',width='content'
        )



