import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from models import session, Usuario


lista_usuarios = session.query(Usuario).all()
#lista_usuarios[0].nome pega o nome - .nome vem da class Usuario que criamos no models.py



#senhas_criptografadas = stauth.Hasher(['12345', '1280', '2004']).generate()

#credenciais ={'usernames':{
#    'fabio@gmail.com':{'name':'Fabio', 'password': senhas_criptografadas[0], 'email': 'fabio@gmail.com'},
#    'joao@gmail.com':{'name':'Joao', 'password': senhas_criptografadas[1], 'email': 'joao@gmail.com'},
#    'alon@gmail.com':{'name':'Alon', 'password': senhas_criptografadas[2], 'email': 'alon@gmail.com'},
#}}
#nas credenciais tem que passar name e password (obrigatorio) #vamos substituir pelo models.py

credenciais = {'usernames': 
               {usuario.email:{'name':usuario.nome, 'password':usuario.senha, 'email':usuario.email} for usuario in lista_usuarios}}

authenticator = stauth.Authenticate(credenciais, 'credenciais_hashco', '5a7uhab91u1hi$a', cookie_expiry_days=30)
#autenticator ja gera a tela de login
#cookie_name - nome do cookies do navegador
#cokkie_key - chave secreta criptografada que armazena no codigo que o usuario final não tem acesso 
#cookie_expiry_day - Quanto tempo o usuario consegue entrar no site sem precisar fazer login varias vezes


def autenticar_usuario(authenticator):
    # Verifica se o resultado não é None e contém três elementos
    nome, status_autenticacao, username = authenticator.login() #devolve 3 valores como resposta - nome do usuario, status de autenticaçao do usuario, username do usuario
    if status_autenticacao:
        #True, False e None (Caso aperte login sem preencher os campos)
        return {'nome': nome, 'username': username}
    elif status_autenticacao == False:
        st.error('Combinação de usuário e senha inválida')
    else:
        st.error('Preencha o formulário para fazer o login')

    
def logout():
    authenticator.logout() #Cria o botao de logout


dados_usuario = autenticar_usuario(authenticator)

if dados_usuario:

    email_usuario = dados_usuario['username']
    usuario = session.query(Usuario).filter_by(email = email_usuario).first() #oda query tem que ter ou .first() ou .all()

    if usuario.admin:

        paginas = st.navigation({
            'Home':[st.Page('homepage.py',title='Hash&Co')],
            'Dashboards':[st.Page('dashboard.py', title='Dashboards'), st.Page('indicadores.py', title='Indicadores')],
            'Conta':[st.Page(logout, title='Sair'), st.Page('criarconta.py', title='Criar conta')]
        })
    else:
        paginas = st.navigation({
            'Home':[st.Page('homepage.py',title='Hash&Co')],
            'Dashboards':[st.Page('dashboard.py', title='Dashboards'), st.Page('indicadores.py', title='Indicadores')],
            'Conta':[st.Page(logout, title='Sair')] #nao tem a opção de criar conta
        })
    paginas.run()
