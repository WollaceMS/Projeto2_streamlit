from models import session, Usuario
import streamlit_authenticator as stauth

senha_criptografada = stauth.Hasher(['12345']).generate()[0]
usuario = Usuario(nome='Wollace3', senha=senha_criptografada, email='wollace3@gmail.com', admin=False)
session.add(usuario)
session.commit()
#não colocar no github esse arquivo py