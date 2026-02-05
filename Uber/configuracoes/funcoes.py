import plotly.io as pio
import pandas as pd
import streamlit as st

def tema_plotly():
    pio.templates['meu_tema'] = pio.templates['plotly_white']

        # paleta de cor.
    pio.templates['meu_tema']['layout']['colorway'] = [
        "#A8E6A3",
        "#8BD7A8",
        "#6AC7AD",
        "#4CB5AE",
        "#3A8FB0",
        "#245A87",
        "#0B2C5F"
    ]
        # niveis da escala.
    pio.templates['meu_tema']['layout']['colorscale'] = {
        'sequential': [
            [0.00, "#A8E6A3"],
            [0.16, "#8BD7A8"],
            [0.33, "#6AC7AD"],
            [0.50, "#4CB5AE"],
            [0.66, "#3A8FB0"],
            [0.83, "#245A87"],
            [1.00, "#0B2C5F"]
        ]
    }

        # atribuindo padrao
    pio.templates.default = 'meu_tema'
@st.cache_data
def abrir_arquivo():
    return pd.read_csv('uber_tratado.csv')



def range_axis(df:pd.DataFrame,col:str,val:int =1,func:str='max'):
    '''
    Gera um valor baseado na fuição escolhida para gerar o valor maximo ou minimo de um eixo  
    
    :param df: A DataFrame a ser utilizada
    :type df: pd.DataFrame
    :param col: A coluna da DataFrame
    :type col: str
    :param val: A constante de correção da altura do eixo. Padrão 1
    :type val: int
    :param func: Valores entre 'mim' ou 'max' que determina se o valor sera o menor ou maior do DataFrame. Padrão 'max'
    :type func: str
    '''
    
    if func == 'min':
        minimo = df[col].min() * val
        return minimo
    if func == 'max':
        maximo = df[col].max() * val
        return maximo