import streamlit as st
from data_loarder import carregar_dados
import plotly.express as px

base = carregar_dados()

coluna_esquerda, coluna_meio, coluna_direita = st.columns([1,1,1])

setor = coluna_esquerda.selectbox('Setor', list(base['Setor'].unique()))
status = coluna_meio.selectbox('Status', list(base['Status'].unique()))

base = base[(base['Setor'] == setor) & (base['Status'] == status)]
base_mensal = base.groupby(base['Data Chegada'].dt.to_period('M')).sum(numeric_only=True).reset_index() #datas do mesmo mês serão agrupadas
#reset_index - indices 0,1,2,3 - padrão

base_mensal['Data Chegada'] = base_mensal['Data Chegada'].dt.to_timestamp() #coluna em forma de data

container = st.container(border=True)
with container:
    #grafico area
    st.write('### Total de Projetos por mês ($)')
    grafico_area = px.area(base_mensal, x = 'Data Chegada', y = 'Valor Negociado')
    st.plotly_chart(grafico_area)

    
    #titulo e filtro do ano
    coluna_esquerda, coluna_direita = st.columns([3,1])

    coluna_esquerda.write('### Total Orçado x Pago')

    base_mensal['Ano'] = base_mensal['Data Chegada'].dt.year
    lista_anos = list(base_mensal['Ano'].unique()) 
    ano_selecionado = coluna_direita.selectbox('Ano', lista_anos)

    #métricas
    base_mensal = base_mensal[base_mensal['Ano'] == ano_selecionado]
    total_pago = base_mensal['Valor Negociado'].sum()
    total_desconto = base_mensal['Desconto Concedido'].sum()

    coluna_esquerda, coluna_direita = st.columns([1,1])
    coluna_esquerda.metric('Total Pago', f'R${total_pago:,.2f}')
    coluna_direita.metric('Total Desconto', f'R${total_desconto:,.2f}')
    #st.table(base_mensal.head(10))

    #grafico de barras
    import plotly.graph_objects as go #criar graficos que não vêm prontos no plotly express

    grafico_barra = go.Figure(data=[
        go.Bar(name='Valor Orçado', x= base_mensal['Data Chegada'], y=base_mensal['Valor Orçado'], text=base_mensal['Valor Orçado']),
        go.Bar(name='Valor Pago', x= base_mensal['Data Chegada'], y = base_mensal['Valor Negociado'], text = base_mensal['Valor Negociado'])
    ])
    grafico_barra.update_layout(barmode='group') #diz que as barras são agrupadas
    st.plotly_chart(grafico_barra) #exibe gráfico

