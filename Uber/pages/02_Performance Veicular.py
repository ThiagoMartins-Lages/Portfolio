import pandas as pd
import streamlit as st
import plotly.express as px
from configuracoes.funcoes import (tema_plotly,abrir_arquivo)


# --- configurando o tema dos gráficos. ---- 

tema_plotly()

# inportando as DF:
df = abrir_arquivo()

# --- Configurando a Página ---
st.set_page_config(
    page_title= "Analise Performance Veiculas",
    page_icon= "🚙",
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

# --- Perguntas de Negócio --- 
# avaliando performance veicular.

tipo_veiculo = df['Tipo de Veículo'].value_counts().reset_index()

# avaliação do deslocamento e valor total de corrida. 

performance_veic_total = df.groupby('Tipo de Veículo')[['Distância da Corrida','Valor da Reserva']].sum().sort_values(by='Distância da Corrida',ascending=False).reset_index()
performance_veic_total['Valor(Rupias)/km'] = performance_veic_total['Valor da Reserva'] / performance_veic_total['Distância da Corrida']
performance_veic_total['₹ Valor da Reserva'] = performance_veic_total['Valor da Reserva'].apply(lambda x: f'₹ {x:,.2f}')
performance_veic_total['₹ Valor(Rupias)/km'] = performance_veic_total['Valor(Rupias)/km'].apply(lambda x: f'₹ {x:,.2f}')


# avaliação do deslocamento e valor médio de corrida. 

performance_veic_med = df.groupby('Tipo de Veículo')[['Distância da Corrida','Valor da Reserva']].mean().sort_values(by='Distância da Corrida',ascending=False).reset_index()
performance_veic_med['Valor(Rupias)/km'] = performance_veic_med['Valor da Reserva'] / performance_veic_med['Distância da Corrida']
performance_veic_med['₹ Valor(Rupias)/km'] = performance_veic_med['Valor(Rupias)/km'].apply(lambda x: f'₹ {x:,.2f}')

# avaliando notas dos veículos e passageiros. 
avaliacao_vaiculo = (
    df.groupby('Tipo de Veículo')[['Avaliação do Motorista','Avaliação do Cliente']].mean().sort_values(by='Avaliação do Motorista').reset_index()
)
avaliacao_vaiculo['Avaliação do Cliente']=avaliacao_vaiculo['Avaliação do Cliente'].round(2)
avaliacao_vaiculo['Avaliação do Motorista']=avaliacao_vaiculo['Avaliação do Motorista'].round(2)

    # Criação da data frame para o Boxplot
df_bxp = df[['Tipo de Veículo','Avaliação do Motorista','Avaliação do Cliente']].copy()
df_bxp = df_bxp.melt(id_vars=['Tipo de Veículo'],var_name='Avaliação Usuario',value_name='Nota')




#--- Layout da Página ---
st.markdown("# :bar_chart: Avaliação da Performance Veicular da Frota Uber Índia")

st.markdown(
    '''
    #### Breve explicação dos Veículos

|**Tipo de veículo**|**Descrição**|
|:------------------|:------------|
|Auto|Rickshaws motorizado, destinados a corridas curtas e econômicas|
|Moto|Serviço de transporte por Motos|
|Go Mini|Categoria econômica de carros compactos|
|Go Sedan|Categoria de carros Sedãs|
|Premier Sedan|Categoria de carros Sedãs de mais alto padrão|
|Uber XL| SUVs e Minivans para grandes grupos e ou grande volume de bagagem|
|eBike| Bicicletas elétricas para aluguel|
|Bike| Motocicletas, utilizadas para deslocamento urbano com agilidade|

    '''
)



with st.expander(label="Performance por Categoria Veicular",expanded=False):
    col_esq, col_dir = st.columns(2)

    with col_esq:
        fig = px.bar(
            data_frame=tipo_veiculo,
            x=tipo_veiculo['Tipo de Veículo'],
            y=tipo_veiculo['count'],
            color='count',
            text='count',
            title= 'Número total de Reservas por Tipo de Carro'
            )
        

        fig.update_yaxes(title_text='Numero de Reservas')

        fig.update_traces(
                textfont= dict(
                    weight='bold'
                )
        )

        fig.update_coloraxes(
            colorbar_title_text='Número de Reservas'
        )

        st.plotly_chart(
            figure_or_data=fig,
            width='stretch'
            )

    with col_dir:
            fig = px.pie(
                data_frame=performance_veic_total,
                values=performance_veic_total['Valor da Reserva'],
                names=performance_veic_total['Tipo de Veículo'],
                title='Relação Receita Total por Tipo Veícular'
            )

            fig.update_traces(
                    textfont= dict(
                    weight='bold'
                    ),
                    hovertemplate='Valor da Reserva: ₹ %{value:,.2f}<br>Tipo de Veículo: %{label}'
            )
        
            st.plotly_chart(
                figure_or_data=fig,
                width='content',
                )

    performance_ord_val = performance_veic_med.sort_values(by='Valor(Rupias)/km',ascending=True)
    fig = px.bar(
        data_frame=performance_ord_val,
        x=performance_ord_val['Tipo de Veículo'],
        y=performance_ord_val['Valor(Rupias)/km'],
        color='Valor(Rupias)/km',
        text='₹ Valor(Rupias)/km',
        title='Valor Médio por Quilômetro Rodado por Tipo de Veículo'
    )

    fig.update_traces(
        textfont=dict(
            weight='bold'
        ),
        hovertemplate='Tipo de Veículo: %{x}<br> Valor(Rupias)/km: ₹ %{y:.2f}'
    )
    fig.update_coloraxes(
            colorbar_title_text='₹ Valor(Rupias)/km'
        )
    fig.update_yaxes(
        tickprefix="₹ ",
        tickformat=",.2f",
    )

    st.plotly_chart(fig,width='stretch')
    with st.expander(label='Análise ✍️'):
        st.markdown(
            '''
            - A partir da observação do Gráfico "**Número total de Reservas por Tipo de Carro**", verifica-se que o Tipo de Veículo Auto concentra o maior volume de corridas reservadas,
            evidenciando uma preferência significativa dos usuários por essa categoria.
            - No entanto, ao analisar o indicador de "**Valor por Quilômetro Rodado por Tipo de Veículo**", identifica-se uma inconsistência na estrutura de precificação:
                - Todos os tipos de veículos apresentam o mesmo valor por quilômetro, o que sugere uma padronização excessiva na política tarifária.
                - Tal uniformidade pode desestimular a permanência de motoristas vinculados a categorias de maior valor agregado (como veículos premium), 
                comprometendo a diversidade da frota e, consequentemente, a qualidade da experiência do usuário final.  
            ''',width='stretch'
        )
with st.expander(label='Avaliação por Categoria'):
    col_esq,col_dir = st.columns(2)
    fig = px.box(
            data_frame=df_bxp,
            x=df_bxp['Avaliação Usuario'],
            y=df_bxp['Nota'],
            title='Distribuição das Avaliações de Clientes e Motoristas'
        )

    fig.update_yaxes(title_text='Notas')
    st.plotly_chart(fig,width='stretch')

    with col_esq:
        fig = px.bar(
            data_frame=avaliacao_vaiculo,
            x=avaliacao_vaiculo['Tipo de Veículo'],
            y=avaliacao_vaiculo['Avaliação do Motorista'],
            text='Avaliação do Motorista',
            title='Média de Notas dos Motoristas',
            color='Avaliação do Motorista'
        )

        fig.update_yaxes(title_text='Notas',range=[1,5])

        fig.update_coloraxes(
            showscale=False
        )
        

        st.plotly_chart(fig,width='content')
        
    with col_dir:
        fig = px.bar(
            data_frame=avaliacao_vaiculo,
            x=avaliacao_vaiculo['Tipo de Veículo'],
            y=avaliacao_vaiculo['Avaliação do Cliente'],
            text='Avaliação do Cliente',
            title='Média de Notas dos Usuarios',
            color='Avaliação do Cliente'
        )
        
        fig.update_coloraxes(
            showscale=False
        )

        fig.update_yaxes(title_text='Notas',range=[1,5])
        st.plotly_chart(fig,width='content')
    
    with st.expander(label='Análise ✍️',expanded=False):
        st.markdown(
            '''
            - No gráfico Distribuição das Avaliações de Clientes e Motoristas, observa‑se que as avaliações dos clientes tendem a apresentar valores superiores. 
            Isso é evidenciado pela mediana mais elevada e pelo menor intervalo interquartil (IQR), indicando menor dispersão. 
            Em contraste, as avaliações dos motoristas mostram maior concentração no segundo quartil, sugerindo distribuição mais assimétrica e maior variabilidade. 
            
            - Observa-se que as médias de avaliação atribuídas tanto pelos motoristas quanto pelos clientes permanecem consistentemente baixas em todas as categorias de veículos, 
            indicando um cenário de insatisfação mútua. Tal insatisfação pode estar associada a fatores como a alta incidência de cancelamentos unilaterais, 
            conforme evidenciado no tópico Perfil de Cancelamento, e à estrutura tarifária excessivamente padronizada entre as categorias. 
            Essa combinação pode contribuir para a desmotivação dos motoristas em relação à plataforma, 
            refletindo-se em avaliações negativas aos passageiros e intensificando o ciclo de cancelamentos.
            ''',width='content'
        )