import streamlit as st


# cointainers - Bloco (caixa) onde coluna inf dentro dele 
# columns - forma de dividir a tela do streamlit
secao_usuario = st.session_state
nome_usuario = None
if 'username' in secao_usuario:
    nome_usuario = secao_usuario.name

coluna_esqueda, coluna_direita = st.columns([1, 1.5])#passa uma lista de colunas - nesse caso são duas colunas, uma maior que a outra

coluna_esqueda.title('Hash&Co')
if nome_usuario:
    coluna_esqueda.write(f'#### Bem-vindo, {nome_usuario}') #markdown

botao_dashboards = coluna_esqueda.button('Dashboards Projetos')
botao_indicadores = coluna_esqueda.button('Principais Indicadores')

if botao_dashboards:
    st.switch_page('dashboard.py')
if botao_indicadores:
    st.switch_page('indicadores.py')

container = coluna_direita.container(border=True) #imagem com borda

container.image('imagens/imagens/time-comunidade.webp')