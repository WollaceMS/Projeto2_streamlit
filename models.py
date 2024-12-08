from sqlalchemy import create_engine, Integer, String, Boolean, Column  
from sqlalchemy.orm import sessionmaker, declarative_base #orm - object relational mapping - Essencialmente, permite que comandos em python façam coisas que o sql faz
#create_session - edita o banco de dados
#declarative_base - classe para criar as tabelas no banco de dados

db =  create_engine('sqlite:///database/meubanco.db')
Session = sessionmaker(bind=db) #cria a sessão
session = Session()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column('id', Integer, primary_key=True, autoincrement=True) #autoincrement - faz automatico o id
    nome = Column('nome', String)
    senha = Column('senha', String)
    email = Column('email', String, nullable=True) #não pode ter o email vazio
    admin = Column('admin', Boolean)

    def __init__(self, nome, senha, email, admin=False): # a função init define o que o usuario tem que passar para criar o usuario
        self.nome = nome #nome do usuario - nome que o usuario passou
        self.senha = senha
        self.email = email
        self.admin = admin



Base.metadata.create_all(bind=db)