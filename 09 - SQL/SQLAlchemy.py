#%%
from sqlalchemy import create_engine


# 1. Engine
'''
O Engine é o ponto de entrada para o SQLAlchemy. Ele gerencia as conexões com o banco de dados.
'''

engine = create_engine('postgresql://postgres:postgres@localhost:5433/teste', echo=True)

print("Conexão estabelecida")
#%%


#2 Declarative Base
#É a classe base da qual todos os seus modelos vão herdar. Pense nela como um "molde" para criar suas tabelas.
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

#3 Modelos (Models)
# São classes Python que representam tabelas no banco de dados. Cada atributo da classe representa uma coluna na tabela.


class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)

#%%
#4. Session
#A Session é usada para gerenciar operações no banco de dados. É como uma "transação" que você abre para fazer várias operações.

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

novo_usuario = Usuario(nome='João', idade=28)
session.add(novo_usuario)
session.commit()

print("Usuário inserido com sucesso.")

#%%
#5. Consultas

usuario = session.query(Usuario).filter_by(nome='João').first()
print(f"Usuário encontrado: {usuario.nome}, Idade: {usuario.idade}")

#5. Relacionamentos
# O SQLAlchemy permite definir relacionamentos entre tabelas, como um-para-muitos, muitos-para-muitos, etc.

#%%
#6. Exemplo de uso sem With

from sqlalchemy.orm import sessionmaker
# assumindo que engine já foi criado

Session = sessionmaker(bind=engine)
session = Session()

try:
    novo_usuario = Usuario(nome='Ana', idade=25)
    session.add(novo_usuario)
    session.commit()
except:
    session.rollback()
    raise
finally:
    session.close()

# Exemplo com With
Session = sessionmaker(bind=engine)

with Session() as session:
    novo_usuario = Usuario(nome='Ana', idade=25)
    session.add(novo_usuario)
    # O commit é feito automaticamente aqui, se não houver exceções
    # O rollback é automaticamente chamado se uma exceção ocorrer
    # A sessão é fechada automaticamente ao sair do bloco with